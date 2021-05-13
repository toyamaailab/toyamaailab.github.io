## Toyama AI Lab Website

- website: https://toyamaailab.github.io/
- repository: https://github.com/toyamaailab/toyamaailab.github.io/

### Usage

1. Update config/AI_SCIPapers_SCI.bib in the repository to refresh the website.
2. Run update.py and upload three new html files to this project.  

  **NOTE: The name of updated file must be "AI_SCIPapers_SCI.bib"**
 
- The format of the AI_SCIPapers_SCI.bib

   The tag of published article are @article and the tag of article in press is @inpress just like follows
   
        ```
        @article{gao2018dendriticcomputation,
            author = "Gao, Shangce and Zhou, MengChu and Wang, Yirui and Cheng, Jiujun and Yachi, Hanaki and Wang, Jiahai",
            title = "Dendritic neuron model with effective learning algorithms for classification, approximation, and prediction",
            journal = "IEEE Transactions on Neural Networks and Learning Systems",
            note = "(Highly Cited Paper, Top 1%)",
            volume = "30",
            number = "2",
            pages = "601--614",
            year = "2019",
            publisher = "IEEE",
            doi = "10.1109/TNNLS.2018.2846646",
            month = "February",
            url = "https://ieeexplore.ieee.org/document/8409490"
        }
        @inpress{cheng2020dynamic,
            author = "Cheng, Jiujun and Cao, Chunrong and Zhou, Mengchu and Liu, Cong and Gao*, Shangce and Jiang, Changjun",
            title = "A Dynamic Evolution Mechanism for IoV Community in an Urban Scene",
            journal = "IEEE Internet of Things Journal",
            year = "2020",
            publisher = "IEEE",
            doi = "10.1109/JIOT.2020.3039775",
            url = "https://ieeexplore.ieee.org/document/9266057"
        }
        ```
   
     The **note** attribute will generate between date and DOI in the website and **url** attribute is the hyperlink 
     of the [PDF].
     
     ```
     Shangce Gao, MengChu Zhou, Yirui Wang, Jiujun Cheng, Hanaki Yachi, and Jiahai Wang, "Dendritic 
     neuron model with effective learning algorithms for classification, approximation, and prediction,
     " IEEE Transactions on Neural Networks and Learning Systems, vol.30, no.2, pp.601-614, February 
     2019. (Highly Cited Paper, Top 1%) DOI: 10.1109/TNNLS.2018.2846646, [PDF] 
     ```
     **NOTE: The order of articles in the bib is just the order of the articles generated in the website**
     
- About online resource downloaded
     
     If you want to add a download link for code and data, just add **resource** attribute to your bibtex like
     ```
    @article{lei2020aggregative,
        author = "Lei, Zhenyu and Gao*, Shangce and Gupta, Shubham and Cheng, Jiujun and Yang, Gang",
        title = "An aggregative learning gravitational search algorithm with self-adaptive gravitational constants",
        journal = "Expert Systems with Applications",
        volume = "152, Article ID 113396, 18 pages",
	       month = "August",
        year = "2020",
        publisher = "Elsevier",
        doi = "10.1016/j.eswa.2020.113396",
        resource = "ALGSA-D30.zip",
        code = "ALGSA-Code.zip",
        resourcebaidu = "https://pan.baidu.com/s/1viLh2haU9E7nRAJeMEWxxw",
        codebaidu = "https://pan.baidu.com/s/1F4BKPkz_6DoWkVfEMVPkqw",
        extraction = "ab12",
        url = "https://www.sciencedirect.com/science/article/abs/pii/S0957417420302207"
     }
    ```
    and upload your file to [resource\\](resource). And it will be generated as an article list with download link in the [sourcedata.html](sourcedata.html). **resourcebaidu** and **codebaidu** are used for Baidu Cloud URL, **extraction** is extraction code of Baidu Cloud URL.
