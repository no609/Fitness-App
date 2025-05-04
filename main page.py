import streamlit as st
import sqlite3
import time
from firebase_admin import credentials
from firebase_admin import auth





cred = credentials.Certificate('/Users/vihaansfolder/All Code Files For Visual /Website/fitness-app-4a1fe-35482cf1a7f9.json')







conn = sqlite3.connect('fitness_app.db')
c = conn.cursor()

# Create a table for storing user information if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()





#countdawn
def count_down(seconds, calories_to_add):
    # Create a placeholder for the countdown
    countdown_placeholder = st.empty()
    
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)  # format specifiers
        time_now = '{:02d}:{:02d}'.format(mins, secs) 
        
        # Updating placeholder
        countdown_placeholder.header(f"{time_now}")
        time.sleep(1)  # Wait for 1 second
        
    countdown_placeholder.header("Time Up! You Did It!")
    
    # Update calories burned in session state
    if 'calories_burned' not in st.session_state:
        st.session_state.calories_burned = 0
    st.session_state.calories_burned += calories_to_add

    
def login():
    st.title("🏋️‍♂️ Home Page")
    st.write("Welcome to the Fitness App! Let's get fit together!")

    if "Username" not in st.session_state:
        st.session_state.Username = ""
    if "Useremail" not in st.session_state:
        st.session_state.Useremail = ""

    if "signedout" not in st.session_state:
        st.session_state.signedout = False
    if "signout" not in st.session_state:
        st.session_state.signout = False

    def f():
        try:
            user = auth.get_user_by_email(Email)
            st.success("Login Successful")
            st.session_state.Username = user.uid
            st.session_state.Useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
        except:
            st.warning("Login Failed")

    def t():
        st.session_state.signedout = False
        st.session_state.signout = False
        st.session_state.Username = ""

    choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])

    if not st.session_state.signedout:
        if choice == 'Login':
            Email = st.text_input("Email")
            Password = st.text_input("Password")
            Username = st.text_input("Enter Username")
            st.button("Login", on_click=f)
        else:
            Email = st.text_input("Email")
            Password = st.text_input("Password")
            Username = st.text_input("Make A Unique Username")

            if st.button("Create Account"):
                user = auth.create_user(email=Email, password=Password, uid=Username)
                st.success("Account Created Successfully!")
                st.write("Login Using Email And Password")

    if st.session_state.signout:
        st.text("Name: " + st.session_state.Username)
        st.button("Sign Out", on_click=t)

            
           
        
    
    
def main():
    
    

    

    if 'calories_burned' not in st.session_state:
        st.session_state.calories_burned = 0

    # Sidebar for navigation
    page = st.sidebar.radio("Select Page", ("Home", "Goal", "Workout", "Calories", "BMI","Recipes"))

    # Initialize session state for choice
    if 'choice_made' not in st.session_state:
        st.session_state.choice_made = False
        

    if page == "Home":
        login()



        

    elif page == "Goal":
        st.title("🎯 Choose Your Goal")

        if 'goal' not in st.session_state:
         st.session_state.goal = "lose"  # default choice

        goal = st.selectbox("Select your fitness goal:", ["gain", "lose"], index=["gain", "lose"].index(st.session_state.goal))
        st.session_state.goal = goal
        st.success(f"You have chosen to {goal} weight!")
        st.session_state.choice_made = True

    elif page == "Workout":
        if st.session_state.choice_made:
            st.title("💪 Your Customized Personalized Plan")
            if st.session_state.goal == "gain":
                st.markdown("Do These Every Day And See Results")
                if st.button("Pushups"):
                    count_down(15,10)
                if st.button("Pullups"):
                    count_down(15,20)
                if st.button("Squats"):
                    count_down(15,20)
                if st.button("Lunges"):
                    count_down(15,15)
                if st.button("Jump Squat"):
                    count_down(15,30)
                if st.button("Plank"):
                    count_down(30,20)
            elif st.session_state.goal == "lose":
                st.markdown("Do These Every Day And See Results In Your Weight")
                st.markdown("Try To Do As Many Exercises As You Can In 15 Seconds")
                if st.button("Mountain Climbers(30kcal)"):
                    count_down(15,30)
                if st.button("Pushups (10)"):
                    count_down(15,10)
                if st.button("Crunches (15)"):
                    count_down(15,15)
                if st.button("Running(for 1 hour,500-600kcal)"):
                     count_down(3600,534)
                if st.button("Skipping(with rope,50-60kcal)"):
                    count_down(120,50)
                
        else:
            st.warning("Please make a choice on the 'Choice' page first.")
    elif page == "Calories":
        st.title("🔥 Calories Burned")
        st.write("###### (To Burn Calories Do The Workouts Till The End Of Timer) ######")
        st.markdown(f"## Total Calories Burned Are {st.session_state.calories_burned} ##")
        if st.session_state.calories_burned >= 600:
            st.write("The Daily Goal Has Been Done")
    elif page == "BMI":
        st.title("📏 BMI Calculator")
        st.markdown("#### BMI, or Body Mass Index, is a number calculated from a person's height and weight, used to estimate body fat #####")
        weight = st.slider("What Is Your Weight(kg): ",10,200)
        height = st.slider("What Is Your Height(cm): ",90,200)
        BMI = (weight)/((height/100)**2)
        st.write(f"Your BMI is: {BMI:.2f}")
        
        st.markdown("### BMI Categories ###")
        st.markdown("**Underweight:** Less than 18.5")
        st.markdown("**Normal weight:** 18.5 - 24.9")
        st.markdown("**Overweight:** 25 - 29.9")
        st.markdown("**Obesity:** 30 or greater")
    
    elif page == "Recipes":
       col1,col2 = st.columns(2, gap= "small", vertical_alignment= "center")
       if st.session_state.choice_made:
            if st.session_state.goal == "gain":
             with col1:
               st.image(r"./avacado.png", width=230)
               st.markdown("### Avocados can be beneficial for weight gain due to their high calorie and healthy fat content ###")
             with col1:
                  st.image(r"./eggs.png",width=230)
                  st.markdown("### Eggs can be a beneficial part of a diet for gaining weight due to their high protein content, healthy fats, and calorie density ###")
            elif st.session_state.goal == "lose":
             with col1:
                 st.image(r"./paneer.png", width=400)
                 st.markdown("### Paneer provides good fats, is high in protein, low in carbohydrates, and prevents our systems from storing as much fat since it contains short-chain fatty acids ###")
             with col1:   
                st.image("./salad.png")
                st.markdown("### Salads are beneficial for weight loss primarily because they are low in calories and high in fiber ###")
       else:
        st.warning("Please make a choice on the 'Choice' page first.")

        
            

        

        
        
        

if __name__ == "__main__":
     main()


conn.close()
