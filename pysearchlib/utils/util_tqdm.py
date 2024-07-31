def set_percent(pbar, current, total=None):
    """
    将 tqdm 的进度手动设置到 current 的位置

    例如:
    current = 20, total =100, 那么显示的就是20%
    current = 10, total =100, 那么显示的就是10%
    current = 50, total =100, 那么显示的就是50%

    demo:
    import time
    import numpy as np
    from tqdm import tqdm
    total = 100
    with tqdm(total=total, ncols=55) as pbar:
        while True:
            progress = np.random.randint(0, total)
            pbar.set_postfix_str(str(progress))
            # pbar.n = num_jobs
            set_percent(pbar, progress, total)
            time.sleep(1)


    Parameters
    ----------
    pbar :
    current :
    total :

    Returns
    -------

    """
    # if current > 0:
    #     pbar.reset(total=total)
    #     pbar.update(current)
    #     pbar.refresh()
    pbar.n = current
    # pbar.reset(total=total)
    # pbar.update(current)
    pbar.refresh()


if __name__ == '__main__':
    import time
    import numpy as np
    from tqdm import tqdm

    total = 100
    with tqdm(total=total, ncols=100) as pbar:
        while True:
            progress = np.random.randint(0, total)
            pbar.set_postfix_str(str(progress))
            # pbar.n = num_jobs
            set_percent(pbar, progress, total)
            tqdm.write("\nsdlfjlsjdf")
            time.sleep(1)
