## Bengali Spelling Correction using Noisy Channel

A web based application for Bengali spelling correction using Noisy Channel method. The documentation and presentation for this repository can be found [here]().

### Pre Requirements

Make sure you have standard `python3.X` installed in your machine. For execution, run the below snippet to your console

```sh
python3 -m venv venv
. venv/bin/active
pip install requirements.txt
pip install https://github.com/kpu/kenlm/archive/master.zip
```

In case you do not have vertual enviornment installed in your machine, I would refer you to follow the standard [pydoc](https://docs.python.org/3/library/venv.html).

### Data Generation

> **Caution**: Data generation can take more than an hour, depending on your computing resoueces. It's always better to use [data_generator.ipynb](), instead below code.

As github has hard limit on file size (i.e. less than 50MB), large datasource files are not included in this repository. To generate remaining large files, follow the below code snippets

```sh
python3 data_processor/download_large_file.py
python3 data_processor/get_sentences.py
python3 data_processor/get_dictionary.py
```

After generating all souce files, a lookup file from the `temp/sentences.txt` file needed to be generated. The lookup file will be used to generate language model probabilities. For generating the lookup fiile (i.e. `.arpa` extension file), refer to the standard documentation given by [Kenneth Heafield](https://kheafield.com/code/kenlm/). 

After all the souce files generation has been done, you need to place the `.arpa` lookup file and the `dictionary.txt` file from the `/temp` folder to the `/assets` folder.

### Run

Now, to run the code in your local enviornment, follow the below snippet (make sure your venv still activated)

```sh
python3 run.py
```

After running the above snippet, your console should generate a localhost Id along with a port number (looks alike 127.0.0.1:5000). Go to your browser, and browse the URL. If all of the above instructions successfully executed, you should see web output as below screenshot

![Demo](/assets/screenshot.jpeg)

### License

Copyright 2024 [@suvasish114](https://suvasish114.github.io)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.