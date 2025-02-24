import time
import datetime
import streamlit as st
from models import generic_response,messages
import os

class GenRobo:
    def __init__(self,saveConversion=True):

        #self.checkQueryRequest('Visualize tesla stock')
        st.set_page_config(layout="wide")
        st.markdown( """<style> .st-emotion-cache-janbn0 { flex-direction: row-reverse; text-align: right; } </style> """, unsafe_allow_html=True, )

        self.saveConversion = saveConversion
        self.intialize_chat_history()
        self.setup_app_interface()

    def __decoding(self,response): 
        try:
            for r in response:
                    for x in r.choices[0].delta.content:
                        time.sleep(0.01)
                        yield x
        except Exception as e:
            pass

    def setup_app_interface(self):
        st.title("ApplAi's Neura")
        self.display_chat_history()
        self.accept_user_input()

    
    def display_chat_history(self):
        for message in st.session_state.messages:
            if message['role'] == 'user':
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            elif message['role'] == 'assistant':
                with st.chat_message(message["role"],avatar='applai logo.png'):
                    st.markdown(message["content"])
            # if message['role'] == 'assistant_image':
            #     blk = message['content']
            #     st.plotly_chart(plot_stock(blk.input['stock_symbol']))
            

    def accept_user_input(self):
        if prompt := st.chat_input("Enter your query:"):
            with st.chat_message("user"):
                st.markdown(prompt)
                if self.saveConversion:
                    self.saveConvTextFile("", f"{prompt}")
                
                
            st.session_state.messages.append({"role": "user", "content": prompt})
            self.generate_response(prompt)
    
    def generate_response(self, user_input):
        with st.spinner("Generating response..."):
            try:
                response= generic_response(user_input)
                self.display_assistant_response(response)
            except:
                with st.chat_message("assistant",avatar='applai logo.png'):
                    st.write("Apologies I am very tired, Please try again later.")

    
    def display_assistant_response(self, response):
        with st.chat_message("assistant",avatar='applai logo.png'):
            try:
                bot_response=st.write_stream(self.__decoding(response))
            except Exception as e: 
                print(e)
                bot_response=st.write('Please Try Again Later')
                bot_response='Please Try Again Later'
                
            if self.saveConversion:
                self.saveConvTextFile("", f"{response}")
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        messages.append({
                "role": "assistant",
                "content": bot_response,
            })
    


    def intialize_chat_history(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # Add greeting message to chat history
            first_message = "Neura: Good Morning. I am Neura, a Smart Assistant for ApplAi's Student Community. How can I assist you today? I can tell you everything about our community and project idea!"
            st.session_state.messages.append({"role": "assistant", "content": first_message})

    # def stream_ans(self,response):
    #     for word in response.split(" "):
    #         yield word + " "
    #         time.sleep(0.05)
    
    def saveConvTextFile(self, filename, text):
        pass
    
    # def checkQueryRequest(self,prompt):
    #     classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")
    #     sequence_to_classify = prompt
    #     candidate_labels = ['Question','Table','Plot']
    #     result = classifier(sequence_to_classify, candidate_labels)
    #     print(result)

if __name__ == "__main__":
    GenRobo(saveConversion=False)
