import google.generativeai as genai

genai.configure(api_key="AIzaSyCVvG89j2wKKpcrchk7eNlBIOk_qzHHbRw")

model = genai.GenerativeModel("gemini-2.5-flash-lite")

print("---chat startedI(type'exit or bye to stop)-----")

while True:
    user_question = input("you:")

    if user_question in ["exit", "bye", "quit"]:
        print("Good Bye")
        break


    response = model.generate_content(user_question)
    print("Agent:", response.text)





