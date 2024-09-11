
# ScrapyProject

This project is a Python-based web scraper built using the Scrapy framework to extract data from the website [tailieu.vn](https://tailieu.vn). The scraper can search for documents on the site by specifying a keyword. It fetches the PDF file of the document.


## Getting Started

To set up the project locally, follow these instructions:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ScrapyProject.git
cd ScrapyProject
```

### 2. Set Up a Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Running the Scrapy Spider

Example command:

```bash
cd crawler
scrapy crawl tailieu -a keyword="toán học"
```

This command will search for documents related to "toán học" (math) on `tailieu.vn` and fetch the PDF file
