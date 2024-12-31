{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"provenance":[],"authorship_tag":"ABX9TyOOgjcnbxqun6H+6vtD4vRa"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","execution_count":3,"metadata":{"colab":{"base_uri":"https://localhost:8080/","height":383},"id":"hEI4-XCdOUuk","executionInfo":{"status":"error","timestamp":1735573789429,"user_tz":-330,"elapsed":1220,"user":{"displayName":"Sarath Peddireddy","userId":"15906184456516676058"}},"outputId":"ec036503-7188-44da-9fc3-3f03b9196f7a"},"outputs":[{"output_type":"error","ename":"ModuleNotFoundError","evalue":"No module named 'streamlit'","traceback":["\u001b[0;31m---------------------------------------------------------------------------\u001b[0m","\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)","\u001b[0;32m<ipython-input-3-cc0e5895857e>\u001b[0m in \u001b[0;36m<cell line: 1>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mrandom\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mrand\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mlangchain\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdocument_loaders\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mWebBaseLoader\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mlangchain\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mprompts\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mPromptTemplate\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mlangchain\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mchains\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mLLMChain\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n","\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'","","\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"],"errorDetails":{"actions":[{"action":"open_url","actionText":"Open Examples","url":"/notebooks/snippets/importing_libraries.ipynb"}]}}],"source":["import streamlit as st\n","import random as rand\n","from langchain.document_loaders import WebBaseLoader\n","from langchain.prompts import PromptTemplate\n","from langchain.chains import LLMChain\n","from langchain.llms import Cohere\n","from langchain.output_parsers import PydanticOutputParser\n","from pydantic import BaseModel, Field\n","import os\n","\n","# Set up the Cohere API key\n","os.environ['COHERE_API_KEY'] = \"buKUyzPzqkyYsaGFvewU9UhLGcdSKy76OF8HdqU9\"\n","\n","# Define the response schema\n","class EmailResponse(BaseModel):\n","    Email_Language: str = Field(description=\"The original language of the mail\")\n","    English_email: str = Field(description=\"The email after translating into English\")\n","    Summary: str = Field(description=\"A 4-bullet-point summary of the email\")\n","    Reply: str = Field(description=\"A polite and professional reply to the email based on the context\")\n","\n","# Initialize the Cohere LLM\n","llm = Cohere(model=\"command-xlarge-nightly\", temperature=0.5)\n","\n","# Define the output parser\n","custom_output_parser = PydanticOutputParser(pydantic_object=EmailResponse)\n","\n","# Define the prompt template\n","template = \"\"\"\n","take the email as input. Email text is {email}\n","{format_instructions}\n","\"\"\"\n","prompt = PromptTemplate(\n","    input_variables=['email', 'format_instructions'],\n","    template=template\n",")\n","\n","# Set up the Streamlit app\n","st.title(\"Email Analysis and Reply App\")\n","st.write(\"Provide an email link or email content, and get insights and a professional reply.\")\n","\n","# Input form for the user\n","with st.form(\"email_form\"):\n","    email_link = st.text_input(\"Enter the email URL (optional):\")\n","    email_content = st.text_area(\"Or paste the email content directly:\")\n","    submit_button = st.form_submit_button(\"Analyze Email\")\n","\n","if submit_button:\n","    try:\n","        if email_link:\n","            # Load email content from the provided URL\n","            loader = WebBaseLoader(email_link)\n","            data = loader.load()\n","            email_text = data[0].page_content\n","        elif email_content:\n","            # Use the provided email content directly\n","            email_text = email_content\n","        else:\n","            st.error(\"Please provide either an email URL or email content.\")\n","            st.stop()\n","\n","        # Create the processing chain\n","        chain = LLMChain(prompt=prompt, llm=llm)\n","\n","        # Invoke the chain to process the email\n","        response = chain.invoke({\n","            'email': email_text,\n","            'format_instructions': custom_output_parser.get_format_instructions()\n","        })\n","\n","        # Parse and display the response\n","        parsed_response = custom_output_parser.parse(response)\n","        st.subheader(\"Email Analysis\")\n","        st.write(f\"**Original Language:** {parsed_response.Email_Language}\")\n","        st.write(f\"**English Email:**\\n{parsed_response.English_email}\")\n","        st.write(\"**Summary:**\")\n","        st.write(parsed_response.Summary)\n","        st.write(\"**Reply:**\")\n","        st.write(parsed_response.Reply)\n","\n","    except Exception as e:\n","        st.error(f\"An error occurred: {e}\")\n"]},{"cell_type":"code","source":[],"metadata":{"id":"rtZkl2hgO8sz"},"execution_count":null,"outputs":[]}]}