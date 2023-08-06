import typing as t
from threading import RLock, Lock
from concurrent.futures import Future

import vapoursynth as vs


T = t.TypeVar("T")


def as_completed(futures: t.Iterable[Future], prefetch: int, backlog: t.Optional[int]=None) -> t.Iterable[T]:
    if backlog is None:
        backlog = prefetch*3
    if backlog < prefetch:
        backlog = prefetch

    enum_fut = enumerate(futures)

    finished = False
    running = 0
    lock = RLock()
    reorder = {}

    def _request_next():
        nonlocal finished, running
        with lock:
            if finished:
                return

            ni = next(enum_fut, None)
            if ni is None:
                finished = True
                return

            running += 1

            idx, fut = ni
            reorder[idx] = fut
            fut.add_done_callback(_finished)

    def _finished(f):
        nonlocal finished, running
        with lock:
            running -= 1
            if finished:
                return

            if f.exception() is not None:
                finished = True
                return
            
            _refill()

    def _refill():
        if finished:
            return

        with lock:
            # Two rules: 1. Don't exceed the concurrency barrier.
            #            2. Don't exceed unused-frames-backlog
            while (not finished) and (running < prefetch) and len(reorder)<backlog:
                _request_next()
    _refill()

    sidx = 0
    try:
        while (not finished) or (len(reorder)>0) or running>0:
            if sidx not in reorder:
                # Spin. Reorder being empty should never happen.
                continue

            # Get next requested frame
            fut = reorder[sidx]

            result = fut.result()
            del reorder[sidx]
            _refill()

            sidx += 1
            yield result

    finally:
        finished = True

class _AOTWrapper:

    def __init__(self, img, alpha):
        self.img = img
        self.alpha = alpha
        
    def planes(self):
        yield from self.img.planes()
        yield from self.alpha.planes()

    def get_stride(self, p):
        i = self.img.format.num_planes
        if p < i:
            return self.img.get_stride(p)
        else:
            return self.alpha.get_stride(0)

def render_alpha_image(frameno, img, alpha):
    f_img = img.get_frame_async(frameno)
    f_alpha = alpha.get_frame_async(frameno)

    o_img = [None]
    o_alpha = [None]
    l = Lock()

    fut = Future()
    def _set_on_error(f):
        if f.exception() is not None:
            fut.set_exception(f.exception())

    def _set(v, f):
        if f.exception() is not None:
            return

        with l:
            v[0] = f.result()
            if o_img[0] is not None and o_alpha[0] is not None:
                fut.set_result(_AOTWrapper(o_img[0], o_alpha[0]))

    f_img.add_done_callback(_set_on_error)
    f_img.add_done_callback(lambda f: _set(o_img, f))

    f_alpha.add_done_callback(_set_on_error)
    f_alpha.add_done_callback(lambda f: _set(o_alpha, f))

    return fut


def encode(
        clip: t.Union[vs.VideoNode, vs.AlphaOutputTuple],
        stream: t.IO[t.ByteString],
        *,
        y4m: bool = False,
        prefetch: t.Optional[int]=None,
        backlog: t.Optional[int]=None,
        progress: t.Optional[t.Callable[[int, int], None]]=None
) -> None:
    if not prefetch:
        prefetch = vs.get_core().num_threads

    if isinstance(clip, vs.AlphaOutputTuple):
        if y4m:
            raise ValueError("cannot output alpha with y4m.")

        # Half the number of prefetch frames as the alpha part will fill an additional slot.
        prefetch = max(1, prefetch // 2)

        frames = (render_alpha_image(frameno, clip[0], clip[1]) for frameno in range(len(clip[0])))
    else:
        frames = (clip.get_frame_async(frameno) for frameno in range(len(clip)))

    if y4m:
        if clip.format.color_family == vs.GRAY:
            y4mformat = 'mono'
            if clip.format.bits_per_sample > 8:
                y4mformat = y4mformat + str(clip.format.bits_per_sample)
        elif clip.format.color_family == vs.YUV:
            if clip.format.subsampling_w == 1 and clip.format.subsampling_h == 1:
                y4mformat = '420'
            elif clip.format.subsampling_w == 1 and clip.format.subsampling_h == 0:
                y4mformat = '422'
            elif clip.format.subsampling_w == 0 and clip.format.subsampling_h == 0:
                y4mformat = '444'
            elif clip.format.subsampling_w == 2 and clip.format.subsampling_h == 2:
                y4mformat = '410'
            elif clip.format.subsampling_w == 2 and clip.format.subsampling_h == 0:
                y4mformat = '411'
            elif clip.format.subsampling_w == 0 and clip.format.subsampling_h == 1:
                y4mformat = '440'
            if clip.format.bits_per_sample > 8:
                y4mformat = y4mformat + 'p' + str(self.format.bits_per_sample)
        else:
            raise ValueError("Can only use vs.GRAY and vs.YUV for V4M-Streams")

        if len(y4mformat) > 0:
            y4mformat = 'C' + y4mformat + ' '

        data = f'YUV4MPEG2 {y4mformat} W{clip.width} H{clip.height} F{clip.fps_num}:{clip.fps_den}Ip A0:0\n'
        stream.write(data.encode("ascii"))

    frame: vs.VideoFrame
    for idx, frame in enumerate(as_completed(frames, prefetch, backlog)):
        if y4m:
            stream.write(b"FRAME\n")

        for planeno, plane in enumerate(frame.planes()):
            # This is a quick fix.
            # Calling bytes(VideoPlane) should make the buffer continuous by
            # copying the frame to a continous buffer
            # if the stride does not match the width*bytes_per_sample.
            if frame.get_stride(planeno) != plane.width*clip.format.bytes_per_sample:
                stream.write(bytes(plane))
            else:
                stream.write(plane)

        if progress is not None:
            progress(idx+1, len(clip))

    stream.close()
