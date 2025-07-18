import json
from bs4 import BeautifulSoup
from datetime import datetime,date







# Convert Jun. 2023 to num. for sort.
def parse_date(date_str):
    return datetime.strptime(date_str, "%b. %Y")

# Sort paper by publication date
def get_paper_order(paper_data):
    time_list = [paper_data[x]['date'] for x in paper_data]

    name_list = [x for x in paper_data]
    dates_with_index = list(enumerate(time_list))
    sorted_dates_with_index = sorted(dates_with_index, key=lambda x: parse_date(x[1]),reverse=True)
    paper_index = [index for index, _ in sorted_dates_with_index]
    paper_data = [data for _, data in sorted_dates_with_index]
    index  = [name_list[x] for x in paper_index]
    return index, paper_data

# Generating html file
def generate_related_work(research_data):

      
    research_data = {k: v for k, v in research_data.items() if k != 'date'}
    paper_index, _ = get_paper_order(research_data)
            


    # Start building HTML
    html_content = f"""
    <!-- Related Work -->
    <div class="bg-gray-100 p-6 rounded-lg shadow-lg">
        <!-- Paper Title -->
        <h3 class="text-2xl font-semibold mb-2 text-gray-900">
            Related Works
        </h3>
        <!-- Related Works  -->
        <div class="text-gray-600 text-sm mb-4">
    """

    ## Add the related works' papers.
    for i, index in enumerate(paper_index):
         html_content += f"""
            <!-- paper items -->
            <div class="text-gray-600 text-base mb-4">
            [{i+1}] {research_data[index]["authors"]},
            <span class="font-semibold">"{research_data[index]['title']}"</span>
            <span class="italic"> {research_data[index]['journal']},</span>
            {research_data[index]['vol']}.
            <a class="text-blue-600 text-lg bg-blue-100 rounded-md px-3 py-1 mr-1 hover:bg-blue-200" href="{research_data[index]["doi"]}" target="_blank"><i class="fas fa-solid fa-book-open"></i> Paper </a>
        </div>
         """


    return html_content


def generate_html(research_data):
    # Start building HTML
    html_content = f"""
    <!-- Research Item -->
    <div class="bg-gray-100 p-6 rounded-lg shadow-lg">
        <!-- Framework Figure -->
        <div class="flex justify-center items-center">
            <img alt="{research_data['imageAlt']}" class="rounded-lg mb-4" height="400" width="600"
                src="{research_data['imageSrc']}" />
        </div>
        <!-- Paper Title -->
        <h3 class="text-lg font-semibold mb-2 text-gray-900">
            {research_data['title']}
        </h3>
        <!-- Author • Journal • Time -->
        <div class="text-gray-600 text-sm mb-4">
    """

    # Authors section
    for i, author in enumerate(research_data['authors']):
        if i == len(research_data['authors'])-1:
            if author['link']:
                html_content += f"""
                and 
                <a class="text-blue-600 hover:underline" target="_blank" href="{author['link']}">
                    {author['name']}
                </a>
                """
            else:
                html_content += f"and {author['name']} "
        else:
            if author['link']:
                html_content += f"""
                <a class="text-blue-600 hover:underline" target="_blank" href="{author['link']}">
                    {author['name']},
                </a>
                """
            else:
                html_content += f"{author['name']}, "

    # Journal and Date section
    html_content += f"""
            •
            <span class="font-semibold">{research_data['journal']}</span>
            • {research_data['date']}
        </div>
        <!-- One sentence introduction to research -->
        <p class="text-gray-600 mb-4">
            {research_data['intro']}
        </p>
        <div class="flex items-center justify-between">
            <!-- Page Views -->
            <div class="flex items-center">
                <i class="fas fa-regular fa-pen-square text-2xl text-gray-400 mr-3"></i>
                <span class="font-semibold text-gray-400">
                    Last edited by {research_data['editor']} • {research_data['editDate']}
                </span>
            </div>
        """
    # <!-- Paper and code link -->
    html_content += """<!-- BibTex, Paper and code link -->
            <div class="flex">"""
    if "BibTex" in research_data:
            html_content += f"""
                <a class="text-blue-600 text-lg bg-blue-100 rounded-md px-5 py-1 mr-2 hover:bg-blue-200"
                    target="_blank"
                    href="https://raw.githubusercontent.com/toyamaailab/toyamaailab.github.io/main/bib/{research_data['BibTex']}"><i class="fas fa-eye"></i> BibTex </a>
            """
    if research_data['paperLink']:
            html_content += f"""
                <a class="text-blue-600 text-lg bg-blue-100 rounded-md px-5 py-1 mr-2 hover:bg-blue-200"
                    target="_blank"
                    href="{research_data['paperLink']}"><i class="fas fa-solid fa-book-open"></i> Paper </a>
            """
    if research_data['codeLink']:
            html_content += f"""
                <a class="text-blue-600 text-lg bg-blue-100 rounded-md px-5 py-1 hover:bg-blue-200"
                    target="_blank" href="{research_data['codeLink']}"> <i class="fab fa-brands fa-github"></i> Code
                </a>
            </div>
        </div>
    </div>
    """

    return html_content

# read the details of denderic learning's paper from json
Paper_data=json.load(open('dendritic.json','r'))

# Sort paper by publication date
paper_index,paper_date = get_paper_order(Paper_data)

# read a HTML template
with open("./config/collections_template.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parsing HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Update the date of this html
times = soup.find(id="update_date")
times.string = 'Update: ' + str(date.today())

## updating items of papers.
# Finding iterms  containers
research_items_container = soup.find("div", id="items")
for i in paper_index:
    # put the new item into html
    
    
    if i == "related_work":
        print(f"Generating html of related_work")
        new_research_item = generate_related_work(Paper_data[i])
    else:
        print(f"Generating html of Paper{i}: ",Paper_data[i]['title'])
        new_research_item = generate_html(Paper_data[i])

    research_items_container.append(BeautifulSoup(new_research_item, "html.parser"))


# ## updating items of papers.
# # Finding iterms  containers
# research_items_container = soup.find("div", id="items")
# for i in paper_index:
#     # put the new item into html
#     print(f"Generating html of Paper{i}:",Paper_data[f"paper{i}"]['title'])
#     new_research_item = generate_html(Paper_data[f"paper{i}"])
#     research_items_container.append(BeautifulSoup(new_research_item, "html.parser"))

# Save the updated html page.
with open("./collections1.html", "w", encoding="utf-8") as file:
    file.write(str(soup))




