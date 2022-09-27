import requests
import queue
import threading
import os
import sys
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit,  unquote, quote
from time import sleep


class GCEScraper:

    def __init__(self, save_path, worker_num=10, worker_delay=0.1, max_size=0, tui=False, attachment_suffix=[".pdf", ".zip"], max_retries=10) -> None:
        self.task_queue = queue.Queue(max_size)
        self.error_queue = queue.Queue(max_size)
        self.state_dict = {i: "" for i in range(0, worker_num)}

        self.tui = tui
        self.save_path = save_path
        self.worker_num = worker_num
        self.worker_delay = worker_delay
        self.attachment_suffix = attachment_suffix
        self.max_retries = 10

        self.terminated = False

    def add_url(self, url_list):
        [self.task_queue.put([url, self.max_retries]) for url in url_list]

    def run(self):
        def update_state_func(i):
            def _update_state(text):
                if self.tui:
                    self.state_dict[i] = text
                else:
                    print("worker " + str(i) + " : " + text)
            return _update_state

        # create workers
        self.workers = [threading.Thread(target=self._worker, args=(
            "worker-" + str(i), self.worker_delay, update_state_func(i))) for i in range(0, self.worker_num)]

        # start workers
        [worker.start() for worker in self.workers]

        if self.tui:
            self.live_display_worker = threading.Thread(
                target=self._live_display)
            self.live_display_worker.start()

        # end
        self.task_queue.join()
        self.terminated = True

        print(list(self.error_queue))
        return list(self.error_queue)

    def _live_display(self):
        sys.stdout.write("\n" * self.worker_num)
        while not self.terminated:
            sleep(0.1)
            # if tui, rewrite multiple lines
            for i in range(0, self.worker_num):
                sys.stdout.write("\x1b[1A\x1b[2K")

            for key in self.state_dict:
                sys.stdout.write("worker" + str(key) + ":\t" +
                                 self.state_dict[key] + "\n")

    def _html_url_handler(self, abs_url) -> list:
        if not abs_url.endswith("/"):
            abs_url += "/"
        page = requests.get(abs_url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = []
        paper_list = soup.find(id="paperslist")
        if paper_list is not None:
            for li in paper_list.find_all("li"):
                results.append(
                    urljoin(abs_url, li.find("a").get("href")))
        else:
            self.error_queue.put(abs_url)

        return results

    def _attachment_url_handler(self, abs_url) -> bool:
        path = os.path.join(self.save_path, unquote(
            urlsplit(abs_url).path[1:]))

        if os.path.exists(path):
            return False

        # not exist, download the file
        file = requests.get(abs_url).content

        # save the file
        dirpath = os.path.split(path)[0]
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(path, "wb") as file_on_disk:
            file_on_disk.write(file)

    def _worker(self, worker_name, delay, update_state):
        while not self.terminated:
            sleep(delay)
            if self.task_queue.empty():
                sleep(1)
                continue

            task = self.task_queue.get()
            if task[1] == 0:
                self.error_queue.put(task[0])
                update_state("GIVEUP " + task[0])
                continue
            else:
                task[1] -= 1

            update_state("GET " + task[0])

            try:
                is_attachment = False
                for suffix in self.attachment_suffix:
                    if task[0].endswith(suffix):
                        is_attachment = True

                if is_attachment:
                    self._attachment_url_handler(task[0])
                else:
                    new_urls = self._html_url_handler(task[0])
                    self.add_url(new_urls)
            except Exception as e:
                self.task_queue.put(task)
                update_state("RETRY " + task[0])

            self.task_queue.task_done()

        print(worker_name + " terminated")


def main():

    parser = argparse.ArgumentParser(description="gcepaper web scraper")
    parser.add_argument("save_location", metavar="path",
                        type=str, help="parent dir to save the scraped files.", default="/")
    parser.add_argument(
        "-t", "--thread", type=int, help="number of parallel workers", metavar="int", default=50)
    parser.add_argument(
        "-d", "--delay", type=float, help="delay after each request", metavar="float",  default=0)
    parser.add_argument("-r", "--retries", type=int,
                        help="maximum retries after giving up a url", metavar="int", default=10)
    parser.add_argument(
        "--tui", help="friendly user interface", action="store_true")
    parser.add_argument("-s", "--suffix", dest="attachment_suffix", type=str,
                        help="url with given suffix will be downloaded", metavar="suffix", nargs="+", default=[".pdf"])

    args = parser.parse_args()

    gce_scraper = GCEScraper(
        args.save_location, worker_num=args.thread, worker_delay=args.delay, tui=args.tui, attachment_suffix=args.attachment_suffix)
    gce_scraper.add_url(
        ["https://papers.gceguide.com/"])

    error_list = gce_scraper.run()

    with open(args.save_location + "scraper_errors.json", "w") as debugfile:
        debugfile.write("\n".join(error_list))


if __name__ == "__main__":
    exit(main())
