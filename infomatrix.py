import streamlit as st
st.set_page_config(page_title="FinRupee",page_icon = "images\\icon.jpg", layout="wide")
import base64
from main_page import main
from AI_Finance_Management import AIFM
from ai_assistant import ai_assistant
from game import game
from stock_price_prediction import stock
from ocr import ocr
from dupont import dupont
from Algo_Strategy import algo_strag
from BI import bi
from Bussiness_Analysts import bussiness_analysts
from Insurance import insurance
from CryptoCurrency import crypto
from banking import bank


def infomatrix():

    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Convert images
    logo_base64 = image_to_base64("images/boblogo.jpeg")
    illustration_base64 = image_to_base64("images/homepage_illus.png")
    aichatbot_base64 = image_to_base64("images/aichatbot.png")
    analysis_base64 = image_to_base64("images/analysis.png")
    compliance_base64 = image_to_base64("images/compliance.png")
    reportgen_base64 = image_to_base64("images/reportgen.png")
    insta_base64 = image_to_base64("images/insta.png")
    git_base64 = image_to_base64("images/git.png")
    linkedin_base64 = image_to_base64("images/linkedin.png")
    discord_base64 = image_to_base64("images/discord.png")


    # # Set page config
    # st.set_page_config(page_title="FinRupee",page_icon = "images/icon.jpg", layout="wide")


    st.sidebar.title("FinRupee")
    page = st.sidebar.radio("Checkout", ["Home", "AI Assistant", "Portfolio", "AI Finance Management","Market Simulation","Expense Retrieval","Dupont Analysis","Algorithm Strategies","Business Intelligence Tool","Business Analysts","Insurance","CryptoCurrency","Unified Banking using Blockchain"])


    def load_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    load_css('style.css')
        
    # Custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;700&display=swap');
        
        body {
            font-family: 'Manrope', sans-serif;
        }
        
        .main-header { 
            color: #000;
            text-shadow: 0px 2px 5.3px rgba(0, 0, 0, 0.19);
            font-family: Manrope;
            font-size: 72px;
            font-style: normal;
            font-weight: 600;
            line-height: 83px; 
            letter-spacing: -2.16px;
            opacity: 0;
            animation: fadeIn 2s forwards;
        }
        
        .experience, .future {
            display: inline-block;
            opacity: 0;
            animation: reveal 1s forwards;
        }
        
        .experience {
            animation-delay: 0.5s;
        }
        
        .future {
            animation-delay: 1s;
            color: #FF5100;
            text-shadow: 0px 2px 5.3px rgba(255, 81, 0, 0.67); 
        }
        
        .sub-header { 
            color: #000;
            text-shadow: 0px 2px 4.1px rgba(0, 0, 0, 0.25);
            font-family: Manrope;
            font-size: 48px;
            font-style: normal;
            font-weight: 500;
            line-height: 83px; /* 172.917% */
            letter-spacing: -1.44px;
            white-space: nowrap;
        }
        
        .sub-header span {
            display: inline-block;
            opacity: 0;
            animation: slideIn 1s 1s forwards;
        }
        
        .sub-header span:nth-child(1) { animation-delay: 1.5s; }
        .sub-header span:nth-child(2) { animation-delay: 1.8s; }
        .sub-header span:nth-child(3) { animation-delay: 2.2s; }
        .sub-header span:nth-child(4) { animation-delay: 2.5s; }
        .sub-header span:nth-child(5) { animation-delay: 2.8s; }
        .sub-header span:nth-child(6) { animation-delay: 2.8s; }
        
        @keyframes reveal {
            from {
                opacity: 0;
                transform: translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            to {
                opacity: 1;
            }
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .fade-in-image {
            opacity: 0;
            animation: fadeIn 1s forwards;
        }
        
        .fade-in-image.image-first {
            animation-delay: 0.5s; /* Delay for the first image */
        }
        
        .fade-in-image.image-second {
            animation-delay: 1s; /* Delay for the second image */
        }
                
    
        
        .svg-divider {
            width: 112%;
            overflow: hidden;
            line-height: 0;
            margin-top: -120px;
            margin-left: -100px;
            box-sizing: content-box;
            padding: 0; 
        }
        
        .svg-divider2 {
            width: 112%;
            overflow: hidden;

            margin-left: -100px;
            box-sizing: content-box;
            padding: 0; 
        }
        
        .svg-divider svg,.svg-divider2 svg {
            position: relative;
            display: block;
            width: 100%;
            height: auto;
            padding: 0;
            margin: 0;
        }
                
        .feature-text {
            color: #FAFAFA;
            text-align: center;
            font-family: 'Manrope', sans-serif;
            font-size: 50px;
            font-style: normal;
            font-weight: 800;
            line-height: 54px; 
            letter-spacing: -1.5px;
            backdrop-filter: blur(7px);
            margin: 40px 0;
            margin-top: -320px;
            visibility: hidden; /* Ensure it's not visible */
            transition: opacity 1.5s ease-in-out, visibility 4.5s ease-in-out;
            animation: textAppear 4s 2s forwards; 
        }
                
        .feature-text2 {
            color: #FAFAFA;
            text-align: center;
            font-family: 'Manrope', sans-serif;
            font-size: 50px;
            font-style: normal;
            font-weight: 800;
            line-height: 54px; 
            letter-spacing: -1.5px;
            backdrop-filter: blur(7px);
            margin: 40px 0;
            margin-top: -350px;
            visibility: hidden; /* Ensure it's not visible */
            transition: opacity 1.5s ease-in-out, visibility 4.5s ease-in-out;
            animation: textAppear 4s 2s forwards; 
        }
                
        .st-emotion-cache-1jicfl2 {
                padding-bottom: 0%;
                }
                
        @keyframes textAppear {
        0% {
            opacity: 0;
            visibility: hidden;
            }
        100% {
            opacity: 1;
            visibility: visible;
            }   
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
        40% {
            transform: translateY(-30px);
            }
        60% {
            transform: translateY(-15px);
            }
        }
        
        
        </style>
        """, unsafe_allow_html=True)


    if page == "Home":
        # Your existing home page content goes here
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"""
                <div class='fade-in-image image-first'>
                    <img src="data:image/png;base64,{logo_base64}" width="300" />
                </div>
                <div class='fade-in text-second'>
                    <h1 class='main-header'>
                        <span class='experience'>Experience the</span><br>
                        <span class='future'>Future of Finance</span>
                    </h1>
                    <p class='sub-header'>
                        <span>Fast,</span>
                        <span>Accurate</span>
                        <span>and</span>
                        <span>Efficient</span>
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='fade-in-image image-second'>
                    <img src="data:image/png;base64,{illustration_base64}" width="700" />
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class='svg-divider'>
                <svg xmlns="http://www.w3.org/2000/svg" width="1512" height="796" viewBox="0 0 1512 796" fill="none">
                    <g filter="url(#filter0_f_3_4)">
                        <path d="M-41.6368 255.518L346.808 340.53H850.059L1538.34 363.084L1643.67 200L1749 352.675V565.117L-157 596L-104.056 413.398L-41.6368 255.518Z" fill="#FF5100" fill-opacity="0.86"/>
                    </g>
                    <defs>
                        <filter id="filter0_f_3_4" x="-357" y="0" width="2306" height="796" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                            <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
                            <feGaussianBlur stdDeviation="100" result="effect1_foregroundBlur_3_4"/>
                        </filter>
                    </defs>
                </svg>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class='feature-text'>
                Robust Features, Exceptional Results
            </div>
        """, unsafe_allow_html=True)


        st.markdown("""
        <style>
        .st-emotion-cache-1jicfl2{
                    padding-right: 0;
                    }
        .card {
        margin-top: -210px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        width: 220px;
        height: 500px;
        box-shadow: 0.5px 0.5px 30px 1px #ff5100;
        padding: 20px;
        overflow: hidden;
        border-radius: 10px;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.320, 1);
        background-color: #ffffff;
        opacity: 0; 
        animation: newfadeIn 3s ease-in-out forwards; 
        animation-delay: 2s;
        margin-bottom: 0px;
        }

        @keyframes newfadeIn {
        from {
            opacity: 0;
            transform: translateY(1000px); 
        }
        to {
            opacity: 1;
            transform: translateY(0); 
        }
        }

        .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        height: 100%;
        text-align: center;
        color: #ff5100;
        }

        .heading {
        font-size: 28px;
        font-family: 'Manrope', sans-serif;
        font-weight: 900;
        line-height: 1.2;
        margin: 0;
        margin-top: 20px;
        letter-spacing: -1.5px;
        backdrop-filter: blur(7px);
        }

        .card__img img {
        max-width: 100%;
        height: auto;
        }

        .card:hover {
        border: 3px solid #ff1500;
        box-shadow: none;
        color: #000;
        }

                    
        .cssbuttons-io-button {
        background: #ff5100;
        color: white;
        font-family: inherit;
        padding: 0.35em;
        padding-left: 1.2em;
        font-size: 16px;
        font-weight: 500;
        border-radius: 0.9em;
        border: none;
        letter-spacing: 0.05em;
        display: flex;
        align-items: center;
        box-shadow: inset 0 0 1.6em -0.6em #fafafa;
        overflow: hidden;
        position: relative;
        height: 2.8em;
        padding-right: 3.3em;
        cursor: pointer;
        }

        .cssbuttons-io-button .icon {
        background: white;
        margin-left: 1em;
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 2.2em;
        width: 2.2em;
        border-radius: 0.7em;
        box-shadow: 0.1em 0.1em 0.6em 0.2em #ff5100;
        right: 0.3em;
        transition: all 0.3s;
        }

        .cssbuttons-io-button:hover .icon {
        width: calc(100% - 0.6em);
        }

        .cssbuttons-io-button .icon svg {
        width: 1.1em;
        transition: transform 0.3s;
        color: #ff5100;
        }

        .cssbuttons-io-button:hover .icon svg {
        transform: translateX(0.1em);
        }

        .cssbuttons-io-button:active .icon {
        transform: scale(0.95);
        }
        
        h3{
                    font-size: 18px;
                    text-align: center;
                    }

        </style>
        """, unsafe_allow_html=True)

        # Create four columns for four cards
        car1, car2, car3, car4 = st.columns(4)

        with car1:
            st.markdown(f"""
            <div class="card">
            <div class="content">
                <p class="heading">Personal Finance Dashboard</p>
                <div class="card__img">
                <img src="data:image/png;base64,{aichatbot_base64}" />
                </div>
                <h3> Know about all your investments at one place</h3>
            </div>
            </div>
            
            """, unsafe_allow_html=True)

        with car2:
            st.markdown(f"""
            <div class="card">
            <div class="content">
                <p class="heading">AI Finance Management</p>
                <div class="card__img">
                <img src="data:image/png;base64,{reportgen_base64}" />
                </div>
                <h3>Take wisely decision using our AI trained models</h3>
            </div>
            </div>
            """, unsafe_allow_html=True)

        with car3:
            st.markdown(f"""
            <div class="card">
            <div class="content">
                <p class="heading">Stock Price Prediction</p>
                <div class="card__img">
                <img src="data:image/png;base64,{analysis_base64}" />
                </div>
                <h3>Get future predictions of Stocks</h3>
            </div>
            </div>
            """, unsafe_allow_html=True)

        with car4:
            st.markdown(f"""
            <div class="card">
            <div class="content">
                <p class="heading">Expense Retrieval</p>
                <div class="card__img">
                <img src="data:image/png;base64,{compliance_base64}" />
                </div>
                <h3> Categorize your bills and expenses seamlessly</h3>
            </div>
            </div>
            """, unsafe_allow_html=True)





        st.markdown("""
            <div class='svg-divider2'>
                <svg xmlns="http://www.w3.org/2000/svg" width="1512" height="796" viewBox="0 0 1512 796" fill="none">
                    <g filter="url(#filter0_f_3_4)">
                        <path d="M-41.6368 255.518L346.808 340.53H850.059L1538.34 363.084L1643.67 200L1749 352.675V565.117L-157 596L-104.056 413.398L-41.6368 255.518Z" fill="#FF5100" fill-opacity="0.86"/>
                    </g>
                    <defs>
                        <filter id="filter0_f_3_4" x="-357" y="0" width="2306" height="796" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix"/>
                            <feBlend mode="normal" in="SourceGraphic" in2="BackgroundImageFix" result="shape"/>
                            <feGaussianBlur stdDeviation="100" result="effect1_foregroundBlur_3_4"/>
                        </filter>
                    </defs>
                </svg>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class='feature-text2'>
                printf("Winners")<br>
                Connect with us 
            </div>
            <div class="footer-card">
                <a class="social-link1" href="https://www.instagram.com/" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <path d="M28.9 9.10004C28.5044 9.10004 28.1177 9.21734 27.7888 9.4371C27.4599 9.65686 27.2036 9.96922 27.0522 10.3347C26.9008 10.7001 26.8612 11.1023 26.9384 11.4902C27.0156 11.8782 27.2061 12.2345 27.4858 12.5143C27.7655 12.794 28.1218 12.9844 28.5098 13.0616C28.8978 13.1388 29.2999 13.0992 29.6653 12.9478C30.0308 12.7964 30.3432 12.5401 30.5629 12.2112C30.7827 11.8823 30.9 11.4956 30.9 11.1C30.9 10.5696 30.6893 10.0609 30.3142 9.68583C29.9391 9.31075 29.4304 9.10004 28.9 9.10004ZM36.5666 13.1334C36.5342 11.7505 36.2752 10.3824 35.8 9.08337C35.3762 7.97193 34.7166 6.9655 33.8666 6.13337C33.0413 5.27908 32.0326 4.62367 30.9166 4.21671C29.6211 3.72698 28.2514 3.46206 26.8666 3.43337C25.1 3.33337 24.5333 3.33337 20 3.33337C15.4666 3.33337 14.9 3.33337 13.1333 3.43337C11.7486 3.46206 10.3789 3.72698 9.08331 4.21671C7.96944 4.62779 6.96154 5.28264 6.13331 6.13337C5.27902 6.95867 4.62361 7.96744 4.21665 9.08337C3.72691 10.3789 3.462 11.7486 3.43331 13.1334C3.33331 14.9 3.33331 15.4667 3.33331 20C3.33331 24.5334 3.33331 25.1 3.43331 26.8667C3.462 28.2515 3.72691 29.6211 4.21665 30.9167C4.62361 32.0326 5.27902 33.0414 6.13331 33.8667C6.96154 34.7174 7.96944 35.3723 9.08331 35.7834C10.3789 36.2731 11.7486 36.538 13.1333 36.5667C14.9 36.6667 15.4666 36.6667 20 36.6667C24.5333 36.6667 25.1 36.6667 26.8666 36.5667C28.2514 36.538 29.6211 36.2731 30.9166 35.7834C32.0326 35.3764 33.0413 34.721 33.8666 33.8667C34.7204 33.0377 35.3805 32.0304 35.8 30.9167C36.2752 29.6177 36.5342 28.2495 36.5666 26.8667C36.5666 25.1 36.6666 24.5334 36.6666 20C36.6666 15.4667 36.6666 14.9 36.5666 13.1334ZM33.5666 26.6667C33.5545 27.7247 33.3629 28.7729 33 29.7667C32.7339 30.492 32.3064 31.1474 31.75 31.6834C31.2094 32.2342 30.5554 32.6608 29.8333 32.9334C28.8395 33.2963 27.7913 33.4879 26.7333 33.5C25.0666 33.5834 24.45 33.6 20.0666 33.6C15.6833 33.6 15.0666 33.6 13.4 33.5C12.3015 33.5206 11.2076 33.3515 10.1666 33C9.47628 32.7135 8.85224 32.288 8.33331 31.75C7.78013 31.2146 7.35805 30.5587 7.09998 29.8334C6.69307 28.8253 6.46739 27.7533 6.43331 26.6667C6.43331 25 6.33331 24.3834 6.33331 20C6.33331 15.6167 6.33331 15 6.43331 13.3334C6.44078 12.2518 6.63823 11.1799 7.01665 10.1667C7.31006 9.46323 7.76042 8.83614 8.33331 8.33337C8.83967 7.76032 9.46546 7.3052 10.1666 7.00004C11.1826 6.63345 12.2533 6.44184 13.3333 6.43337C15 6.43337 15.6166 6.33337 20 6.33337C24.3833 6.33337 25 6.33337 26.6666 6.43337C27.7246 6.44551 28.7728 6.63712 29.7666 7.00004C30.524 7.28113 31.2038 7.73812 31.75 8.33337C32.2961 8.84534 32.7229 9.47126 33 10.1667C33.3704 11.1816 33.5621 12.253 33.5666 13.3334C33.65 15 33.6666 15.6167 33.6666 20C33.6666 24.3834 33.65 25 33.5666 26.6667ZM20 11.45C18.3097 11.4533 16.6582 11.9576 15.2544 12.8991C13.8506 13.8406 12.7573 15.177 12.1127 16.7396C11.4681 18.3022 11.3012 20.0208 11.633 21.6783C11.9648 23.3357 12.7804 24.8576 13.9768 26.0517C15.1732 27.2457 16.6967 28.0584 18.3547 28.387C20.0128 28.7155 21.7311 28.5452 23.2924 27.8976C24.8538 27.25 26.1881 26.1541 27.1269 24.7484C28.0656 23.3428 28.5666 21.6904 28.5666 20C28.5689 18.8752 28.3487 17.7611 27.9187 16.7216C27.4888 15.6822 26.8576 14.7381 26.0614 13.9435C25.2653 13.1489 24.3199 12.5195 23.2796 12.0916C22.2394 11.6637 21.1248 11.4456 20 11.45ZM20 25.55C18.9023 25.55 17.8293 25.2245 16.9166 24.6147C16.0039 24.0049 15.2925 23.1381 14.8724 22.1239C14.4524 21.1098 14.3425 19.9939 14.5566 18.9173C14.7708 17.8407 15.2994 16.8518 16.0755 16.0756C16.8517 15.2994 17.8406 14.7708 18.9172 14.5567C19.9938 14.3425 21.1097 14.4524 22.1239 14.8725C23.138 15.2926 24.0048 16.0039 24.6146 16.9166C25.2245 17.8293 25.55 18.9024 25.55 20C25.55 20.7289 25.4064 21.4506 25.1275 22.1239C24.8486 22.7973 24.4398 23.4091 23.9244 23.9245C23.4091 24.4398 22.7972 24.8487 22.1239 25.1276C21.4505 25.4065 20.7288 25.55 20 25.55Z" fill="#FF1500"/>
                    </svg>
                </a>
                <a class="social-link2" href="https://www.github.com/" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M20 3.33337C10.7916 3.33337 3.33332 10.7917 3.33332 20C3.33143 23.4988 4.43134 26.9094 6.47701 29.7478C8.52268 32.5863 11.4102 34.7085 14.73 35.8134C15.5633 35.9584 15.875 35.4584 15.875 35.02C15.875 34.625 15.8533 33.3134 15.8533 31.9167C11.6666 32.6884 10.5833 30.8967 10.25 29.9584C10.0616 29.4784 9.24998 28 8.54165 27.6034C7.95832 27.2917 7.12498 26.52 8.51998 26.5C9.83332 26.4784 10.77 27.7084 11.0833 28.2084C12.5833 30.7284 14.98 30.02 15.9366 29.5834C16.0833 28.5 16.52 27.7717 17 27.355C13.2916 26.9384 9.41665 25.5 9.41665 19.125C9.41665 17.3117 10.0616 15.8134 11.125 14.6467C10.9583 14.23 10.375 12.5217 11.2916 10.23C11.2916 10.23 12.6866 9.79171 15.875 11.9367C17.2318 11.5607 18.6337 11.3717 20.0416 11.375C21.4583 11.375 22.875 11.5617 24.2083 11.9367C27.395 9.77004 28.7916 10.23 28.7916 10.23C29.7083 12.5217 29.125 14.23 28.9583 14.6467C30.02 15.8134 30.6666 17.2917 30.6666 19.125C30.6666 25.5217 26.7716 26.9384 23.0633 27.355C23.6666 27.875 24.1883 28.875 24.1883 30.4384C24.1883 32.6667 24.1666 34.4584 24.1666 35.0217C24.1666 35.4584 24.48 35.9784 25.3133 35.8117C28.6217 34.6947 31.4965 32.5684 33.5332 29.732C35.5698 26.8956 36.6657 23.4919 36.6666 20C36.6666 10.7917 29.2083 3.33337 20 3.33337Z" fill="#FF1500"/>
                    </svg>
                    </a>
                <a class="social-link3" href="https://www.discord.com/" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <path d="M31.57 9.26005C29.3842 8.23551 27.0716 7.50687 24.6933 7.09338C24.3685 7.68914 24.0742 8.30105 23.8116 8.92672C21.2856 8.54236 18.716 8.54236 16.19 8.92672C15.9241 8.30084 15.6265 7.68894 15.2983 7.09338C12.9183 7.50644 10.604 8.23509 8.41664 9.26005C4.56708 14.9663 2.87276 21.8559 3.63664 28.6967C6.12347 30.5758 8.92415 31.9984 11.9083 32.8984C12.5928 31.9573 13.195 30.9656 13.715 29.9234C12.7278 29.5482 11.7762 29.0852 10.8716 28.54C11.1105 28.3623 11.3428 28.1784 11.5683 27.9884C14.1986 29.2551 17.0805 29.9128 20 29.9128C22.9194 29.9128 25.8013 29.2551 28.4316 27.9884C28.6605 28.1795 28.8928 28.3634 29.1283 28.54C28.2205 29.0867 27.2705 29.5489 26.2783 29.9267C26.7972 30.9667 27.4015 31.9617 28.085 32.9017C31.1275 31.9597 33.9833 30.4963 36.525 28.5767C37.2234 21.7534 35.4666 14.9046 31.57 9.26005ZM14.4633 24.6884C13.6157 24.6284 12.8258 24.2372 12.2644 23.5994C11.703 22.9616 11.4152 22.1284 11.4633 21.28C11.4099 20.4301 11.6957 19.5936 12.258 18.9541C12.8204 18.3145 13.6135 17.9241 14.4633 17.8684C14.8849 17.8938 15.2972 18.0024 15.6766 18.188C16.056 18.3735 16.3949 18.6323 16.6738 18.9495C16.9527 19.2666 17.166 19.6358 17.3015 20.0358C17.437 20.4358 17.492 20.8587 17.4633 21.28C17.5158 22.1295 17.2296 22.9651 16.6673 23.6039C16.1051 24.2427 15.3125 24.6327 14.4633 24.6884ZM25.5366 24.6884C24.6891 24.6284 23.8991 24.2372 23.3377 23.5994C22.7763 22.9616 22.4885 22.1284 22.5366 21.28C22.4832 20.4301 22.769 19.5936 23.3314 18.9541C23.8938 18.3145 24.6868 17.9241 25.5366 17.8684C25.9582 17.8938 26.3706 18.0024 26.7499 18.188C27.1293 18.3735 27.4682 18.6323 27.7471 18.9495C28.026 19.2666 28.2393 19.6358 28.3748 20.0358C28.5104 20.4358 28.5653 20.8587 28.5366 21.28C28.5892 22.1295 28.303 22.9651 27.7407 23.6039C27.1784 24.2427 26.3859 24.6327 25.5366 24.6884Z" fill="#FF1500"/>
                    </svg>
                </a>
                <a class="social-link4" href="https://www.linkedin.com/" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <g clip-path="url(#clip0_32_236)">
                    <path d="M34.0783 34.0867H28.155V24.805C28.155 22.5917 28.11 19.7433 25.0683 19.7433C21.98 19.7433 21.5083 22.1517 21.5083 24.6417V34.0867H15.585V15H21.275V17.6017H21.3517C22.1467 16.1017 24.08 14.5183 26.9683 14.5183C32.97 14.5183 34.08 18.4683 34.08 23.61L34.0783 34.0867ZM8.895 12.3883C8.44301 12.389 7.99533 12.3004 7.57766 12.1276C7.15998 11.9549 6.78053 11.7013 6.46108 11.3816C6.14163 11.0618 5.88846 10.6821 5.71609 10.2643C5.54373 9.84642 5.45557 9.39866 5.45667 8.94667C5.457 8.2663 5.65907 7.60131 6.03734 7.03579C6.4156 6.47026 6.95307 6.02961 7.58178 5.76955C8.21048 5.50949 8.90218 5.4417 9.56941 5.57476C10.2366 5.70781 10.8494 6.03574 11.3303 6.51707C11.8112 6.99839 12.1385 7.6115 12.2709 8.27886C12.4033 8.94622 12.3348 9.63785 12.0742 10.2663C11.8135 10.8948 11.3723 11.4318 10.8064 11.8095C10.2406 12.1872 9.57537 12.3887 8.895 12.3883ZM11.865 34.0867H5.925V15H11.865V34.0867ZM37.0417 0H2.95167C1.32 0 0 1.29 0 2.88167V37.1183C0 38.7117 1.32 40 2.95167 40H37.0367C38.6667 40 40 38.7117 40 37.1183V2.88167C40 1.29 38.6667 0 37.0367 0H37.0417Z" fill="#FF1500"/>
                    </g>
                    <defs>
                    <clipPath id="clip0_32_236">
                    <rect width="40" height="40" fill="white"/>
                    </clipPath>
                    </defs>
                    </svg> 
                </a>
            </div>

        """, unsafe_allow_html=True)

        st.markdown("""
        <style>
        .footer-card {
            display: flex;
            height: 70px;
            width: 350px;
            margin: 0 auto;
            bottom: 20px;
            left: 0;
            right: 0;
            justify-content: center;
        }

        .footer-card svg {
            position: absolute;
            display: flex;
            width: 50%;
            height: 100%;
            font-size: 24px;
            font-weight: 700;
            opacity: 1;
            transition: opacity 0.25s;
            z-index: 2;
            padding: 0.25rem;
            cursor: pointer;
        }

        .footer-card .social-link1, .footer-card .social-link2, .footer-card .social-link3, .footer-card .social-link4{
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 25%;
            color: whitesmoke;
            font-size: 24px;
            text-decoration: none;
            transition: 0.25s;
            border-radius: 10px;
        }

        .footer-card svg {
            transform: scale(1);
        }

        .footer-card .social-link1:hover {
            background: #f09433;
            background: -moz-linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
            background: -webkit-linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);
            background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%);
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#f09433', endColorstr='#bc1888', GradientType=1);
            animation: bounce_613 0.2s linear;
        }
                    
        .footer-card .social-link1:hover svg path {
            fill: #ffffff; 
            }

        .footer-card .social-link2:hover {
            background-color: #242c34;
            animation: bounce_613 0.2s linear;
        }

            .footer-card .social-link2:hover svg path {
            fill: #ffffff; 
            }         

        .footer-card .social-link3:hover {
            background-color: #5865f2;
            animation: bounce_613 0.2s linear;
        }
            .footer-card .social-link3:hover svg path {
            fill: #ffffff; 
            }

        .footer-card .social-link4:hover {
            background-color: #0a66c2;
            animation: bounce_613 0.2s linear;
        }
            .footer-card .social-link4:hover svg path {
            fill: #ffffff; 
            }
                    
        .sidebar .sidebar-content {
            background-color: #f1f3f6;
        }
        
        .sidebar .sidebar-content .block-container {
            padding-top: 2rem;
        }
        
        .sidebar .sidebar-content .stRadio > label {
            font-size: 1.2rem;
            font-weight: 600;
            color: #333;
        }
        
        .sidebar .sidebar-content .stRadio > div {
            margin-top: 1rem;
        }
        
        }
        </style>
        """, unsafe_allow_html=True)   

    elif page == "Portfolio":  
        main()
    elif page == "AI Finance Management":
        AIFM()
    elif page == "AI Assistant":
        ai_assistant()
    elif page == "Market Simulation":
        game()
    elif page == 'Stock Price Prediction':
        stock()
    elif page == "Expense Retrieval":
        ocr()
    elif page == "Dupont Analysis":
        dupont()
    elif page == "Algorithm Strategies":
        algo_strag()
    elif page == "Business Intelligence Tool":
        bi()
    elif page == "Business Analysts":
        bussiness_analysts()
    elif page == "Insurance":
        insurance()
    elif page == "CryptoCurrency":
        crypto()
    elif page == 'Unified Banking using Blockchain':
        bank()

if __name__ == "__main__":
    infomatrix()
