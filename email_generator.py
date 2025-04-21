# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_core.output_parsers import JsonOutputParser

# llm = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     temperature=0,
#     groq_api_key = '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',
    
# )
# res = llm.invoke("generate a python code of addition and explain me in detail as well")
# loader = WebBaseLoader("https://explore.jobs.netflix.net/careers/job/790299385411")
# page_data = loader.load().pop().page_content
# prompt_extract = PromptTemplate.from_template(
#     """
#     ### SCRAPED TEXT FROM WEBSITE:
#     {page_data}
#     ### INSTRUCTION:
#     The scraped text is from the career's page of a website.
#     Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`,`skills` and `description`.
#     Only return the valid JSON.
#     ### VALID JSON (NO PREAMBLE):
#     """
# )
# chain_extract = prompt_extract | llm
# res = chain_extract.invoke(input={'page_data':page_data})
# json_parser = JsonOutputParser()
# json_res = json_parser.parse(res.content)
# # print(json_res)
# import pandas as pd
# df = pd.read_csv('portfolio.csv')
# # print(df)
# import chromadb
# import uuid
# client = chromadb.PersistentClient('vectorstore')
# collection = client.get_or_create_collection(name="portfolio")
# if not collection.count():
#     for _, row in df.iterrows():
#         collection.add(documents=row["Techstack"],
#                        metadatas={"links": row["Links"]},
#                        ids=[str(uuid.uuid4())])
# job = json_res[]
# link = collection.query(query_texts=job['skills'], n_results=2).get('metadatas', [])
# print(link)
# print(job['skills'])
# prompt_email = PromptTemplate.from_template(
#     """ 
#     ### JOB DESCRIPTION:
# {job_description}
# ### INSTRUCTION:
# You are Priya, a business development executive at Nexora. Nexora is a cutting-edge technology firm specializing in AI-powered solutions and bespoke software development.
# Over the years, Nexora has transformed numerous businesses by delivering innovative tools that drive operational efficiency, enhance customer experiences, and enable sustainable growth.
# Your task is to write a cold email to a prospective client regarding the job mentioned above, highlighting Nexora's expertise in addressing their requirements.
# Additionally, include the most relevant examples from the following links to showcase Nexora's portfolio: {link_list}.
# Remember, you are Priya, BDE at Nexora.
# Do not provide a preamble
# ### EMAIL (NO PREAMBLE):
#     """
   
# )
# chain_email = prompt_email | llm
# res1 = chain_email.invoke({"job_description":str(job), "link_list": link})
# print(res1.content)
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
import chromadb
import uuid

# -------------------- Step 1: Setup LLM --------------------
llm = ChatGroq(
    model="llama3-70b-8192",  # Fix model name to Groq-supported one
    temperature=0,
    groq_api_key='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',
)

# -------------------- Step 2: Scrape job posting --------------------
loader = WebBaseLoader("http://joinus.decathlon.in/en/annonce/3649799-lead-java-developer-bengaluru")
page_data = loader.load().pop().page_content

# -------------------- Step 3: Extract job fields in JSON --------------------
prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    The scraped text is from the career's page of a website.
    Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, and `description`.
    Only return the valid JSON.
    ### VALID JSON (NO PREAMBLE):
    """
)
chain_extract = prompt_extract | llm
res = chain_extract.invoke(input={'page_data': page_data})

# -------------------- Step 4: Parse JSON safely --------------------
json_parser = JsonOutputParser()
json_res = json_parser.parse(res.content)

# Ensure it's a list (multiple jobs) or a single job
job = json_res[0] if isinstance(json_res, list) else json_res

# -------------------- Step 5: Load portfolio CSV and create ChromaDB vectorstore --------------------
df = pd.read_csv('portfolio.csv')

client = chromadb.PersistentClient('vectorstore')
collection = client.get_or_create_collection(name="portfolio")

if not collection.count():
    for _, row in df.iterrows():
        collection.add(
            documents=[row["Techstack"]],
            metadatas={"links": row["Links"]},
            ids=[str(uuid.uuid4())]
        )

# -------------------- Step 6: Query ChromaDB with job skills --------------------
skills = job['skills']
if isinstance(skills, str):
    skills = [s.strip() for s in skills.split(',')]

result = collection.query(query_texts=skills, n_results=2)
link = result.get('metadatas', [])

# -------------------- Step 7: Cold email generation --------------------
prompt_email = PromptTemplate.from_template(
    """ 
    ### JOB DESCRIPTION:
{job_description}
### INSTRUCTION:
You are Priya, a business development executive at Nexora. Nexora is a cutting-edge technology firm specializing in AI-powered solutions and bespoke software development.
Over the years, Nexora has transformed numerous businesses by delivering innovative tools that drive operational efficiency, enhance customer experiences, and enable sustainable growth.
Your task is to write a cold email to a prospective client regarding the job mentioned above, highlighting Nexora's expertise in addressing their requirements.
Additionally, include the most relevant examples from the following links to showcase Nexora's portfolio: {link_list}.
Remember, you are Priya, BDE at Nexora.
Do not provide a preamble
### EMAIL (NO PREAMBLE):
    """
)

chain_email = prompt_email | llm
res1 = chain_email.invoke({"job_description": str(job), "link_list": link})
print(res1.content)