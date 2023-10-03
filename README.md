# Recommendor

Here you may find the code for the license thesis I have written during my 3rd year at Babes-Bolyai University in 2023. 

Other parts of my license thesis such as the application itself or the thesis itself can be found on the [application's site](http://www.musicsimilarity.com/ "Application Site"). 

The dataset was created by me and can be found [here]() and the trained models used are uploaded [here](). 

You may observe that we do not use a secure connection, which is an issue to be fixed soon in the future.

## Fair Use Disclaimer

The dataset contains copyrighted songs that are used for research purposes only. We do not earn any money from the use of these copyrighted materials. Our use of these songs falls under the doctrine of "Fair Use" as defined in Section 107 of the United States Copyright Act.

### Fair Use Factors Considered:

#### Purpose and Character of Use

The use of copyrighted songs in the application is for research and educational purposes. 

We do not derive any commercial benefit from the inclusion of these songs. 

This transformative use serves to enhance the understanding and analysis of the music, making it eligible for fair use protection.

#### Nature of the Copyrighted Work

We use copyrighted songs, which are creative and expressive works. 

However, our use is for non-commercial, research-oriented purposes and does not compete with the original market for these songs.

#### Amount and Substantiality of the Portion Used

We use only a limited portion of each song, typically for analysis purposes, and do not use the entirety of the copyrighted material.

#### Effect on the Potential Market

Our use of these songs does not adversely affect the market value of the original works. 

We do not offer the songs for download, sale, or any form of commercial distribution.


We acknowledge the rights of the copyright holders and make every effort to provide proper attribution where necessary.

If you are the copyright owner of any of the songs used in the dataset and believe that your rights have been infringed upon, please contact us, and we will promptly address your concerns by either removing the content or providing appropriate attribution as required.

Please understand that our use of copyrighted songs is in accordance with the principles of fair use for research and educational purposes and is not intended for commercial gain.

## Overview

The basic idea behind the used algorithm was to use the Encoder-Decoder architecture of a Transformer for the purpose of classifying songs into musical subgenres.

As musical subgenres are subjective, I have decided that, instead of using one tag per song, a probability density function would be obtained in order to represent the membership of a song to a given genre.

Using previous user data regarding similarity of subgenres, several subgenres are chosen as the best candidates for a song and songs of those subgenres are presented.

For more details on how the algorithm works, please visit the paper from the site.

## Calin (Server)

The name of the server coincides with my name for the purpose of choosing a random name.

The server was written solely in Kotlin.

The purpose of the server is to store similarity data which is given by demo users as input data, modify user data and recommend songs to regular users using the algorithm.

The server communicates with the front-end of the application using REST API.

The server also communicates with the Recommender Server, written in Python, using TCP and message conventions maintained throughout the application.

## Demo-Client (Frontend)

The purpose of the frontend is to create a bridge between the server and the users.

The frontend was written in Angular.

The frontend also uses different environments, depending on whether it is deployed or not.

## Recommendor

This folder contains several different files, each serving different purposes, though the general purpose is to train the several models used in the application.

The audio file interpreters are also stored here, which translates a song from an audio file to a matrix of integer values.

All models which were trialed for the issue at hand can be found in `model/`.

`runners/` contains scripts which were run at some point during the training of the models. For more details, check the paper.

## Scripts

Python scripts which had to be run only a few times are included in this folder. 

For example, `data_extractor.py` downloads the songs from YouTube in order for me to not do it manually.

`migration_creator.py` then creates a database using those songs and their tags, taken from the `.csv` files.

`server.py` waits for changes indicated by a notification, then reloads the similarity matrices which were changed.

`rating_extractor.py` extracts from the database the ratings and processes them, and afterwards, it notifies the `server.py` which is continuously running.

## Services

This folder contains services which run continuously on the Linux Virtual Machine, or their helpers.   

Using Facade pattern, `main.py` is the principal part of the folder, representing the Recommender Python service communicating with the Kotlin server.

The purpose of each file can be derived from their suggestive names.

## Shared

Files which were used in multiple modules where put there in order for Python to understand that it is the same class that it is being talked about.

# License

This software is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). 

You may obtain a copy of the license at the provided link or by contacting the Apache Software Foundation.

Unless required by applicable law or agreed to in writing, software distributed under the Apache 2.0 License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
