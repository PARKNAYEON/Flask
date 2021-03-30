# Asyncio
# 비동기 I/O Coroutine 작업
# Generator -> 반복적인 객체 Return(yield)
# 즉, 실행 stop -> 다른 작업으로 위임 -> stop 지점부터 재실행 원리
# Non-Blocking 비동기 처리에 적합

# BlockIO -> Thread 염두
# 쓰레드 개수 및 GIL 문제 염두, 공유 메모리 문제 해결

import timeit
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
import threading 


urls = ['https://daum.net', 'https://google.com', 'https://apple.com', 'https://tistory.com', 'https://github.com', 'https://gmarket.co.kr']


start = timeit.default_timer()


def fetch(url):
    print('Thread Name : ', threading.current_thread().getName(), 'Start', url)
    urlopen(url)
    print('Thread Name : ', threading.current_thread().getName(), 'Done', url)

def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            executor.submit(fetch, url)

if __name__ == '__main__':
    # 함수 실행
    main()

    # 완료시간 - 시작시간
    duration = timeit.default_timer() - start

    # 총 실행 시간
    print('Total time : ', duration)