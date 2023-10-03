import pathlib
import subprocess
import logging
import pandas as pd
import scipy.io.wavfile as wavfile
import os
# TODO: stdin stdout stderr to log or something


class Extractor:
    index: int = 0
    template: str = "audio_{}.wav"
    general_headers = ["general genre", "filename"]
    specific_headers = ["specific genre", "filename"]
    data_folder = "data"
    tags_folder = "tags"
    temp_format = "m4a"
    exec_name = "yt-dlp"

    def __init__(self):
        logging.basicConfig(
            filename="../log.txt",
            level=logging.INFO,
            format='%(asctime)s: %(message)s'
        )

    @staticmethod
    def bytes_to_str(bytes_seq):
        return bytes_seq.decode('utf-8')

    @staticmethod
    def download_song(url: str, output: str):
        result = subprocess.run(
            [Extractor.exec_name, "--rm-cache-dir"],
            capture_output=True
        )
        if result.returncode != 0:
            logging.warning(f"Error when clearing youtube-dl cache: {Extractor.bytes_to_str(result.stderr)}")
            return True

        logging.info(f"Successfully cleared youtube-dl cache")
        logging.info(f"Downloading {url} to {output}...")
        print(f"Downloading {url}")
        result = subprocess.run(
            [Extractor.exec_name, "--extract-audio", "--audio-format", Extractor.temp_format, "--output", f"{output}_temp.{Extractor.temp_format}", url],
            capture_output=True
        )
        if result.returncode != 0:
            logging.warning(f"Error when downloading {url}: {Extractor.bytes_to_str(result.stderr)}")
            return True

        logging.info(f"Downloaded {url} to {output} successfully")
        result = subprocess.run(
            ["ffmpeg", "-i", f"{output}_temp.{Extractor.temp_format}", f"{output}.wav"],
            capture_output=True
        )

        temp_file = pathlib.Path(f"{output}_temp.{Extractor.temp_format}")
        temp_file.unlink()
        logging.info(f"Deleted temporary file {output}_temp.{Extractor.temp_format}")
        if result.returncode != 0:
            logging.warning(f"Error when converting {output}_temp.{Extractor.temp_format} to wav file: {Extractor.bytes_to_str(result.stderr)}")
            return True

        logging.info(f"Successfully converted {output}_temp.{Extractor.temp_format} to wav file")
        return False

    def extract_clips(self, filename, clip_length=30):
        rate, data = wavfile.read(f"{filename}.wav")
        logging.info(f"Extracting f{filename}.wav in 30 second clips")
        data = data[rate * 15:-rate * 15]
        # remove first and last 15 seconds

        clip_start = 0
        while clip_start + rate * clip_length < len(data):
            clip = data[clip_start:clip_start + rate * clip_length]
            clip_filename = os.path.join(self.data_folder, self.template.format(self.index))
            self.index += 1
            logging.info(f"Extracted clip of file {filename}.wav to {clip_filename}")
            wavfile.write(clip_filename, rate, clip)
            clip_start += rate * clip_length

        path = pathlib.Path(f"{filename}.wav")
        path.unlink()
        logging.info(f"Deleted temporary file {filename}.wav")

    def extract_all_files(self, in_csv, out_csv):
        df = pd.read_csv(in_csv)
        rows = df.shape[0]
        for i in range(rows):
            general_csv_data = []
            specific_csv_data = []
            general_genre = df.iloc[i]['general genre']
            specific_genre = df.iloc[i]['specific genre']
            url = df.iloc[i]['url']
            start_index_incl = self.index

            temp_path = f"temp_{i}"
            downloaded_successfully = False
            while not downloaded_successfully:
                downloaded_successfully = not self.download_song(url, temp_path)

            self.extract_clips(temp_path)
            end_index_excl = self.index
            for j in range(start_index_incl, end_index_excl):
                general_csv_data.append([general_genre, self.template.format(j)])
                specific_csv_data.append([specific_genre, self.template.format(j)])

            general_out_df = pd.DataFrame(general_csv_data, columns=self.general_headers)
            specific_out_df = pd.DataFrame(specific_csv_data, columns=self.specific_headers)
            general_out_df.to_csv(os.path.join(self.tags_folder, out_csv), mode='a', index=False, header=False)
            specific_out_df.to_csv(os.path.join(self.tags_folder,  f"{general_genre}_{out_csv}"), mode='a', index=False, header=False)


def extract():
    extractor = Extractor()
    extractor.extract_all_files("genres.csv", "out_genres.csv")

if __name__ == "__main__":
    extract()
