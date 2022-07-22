from functions_used import download_subtitles, time_limit, main_matcher, question_answer
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

user_answers=[]
answers=[]
questions=[]

@app.route('/', methods=['GET', 'POST'])
def home():
    global video_id
    if request.method == 'POST':
        video_id = request.form.get('video_id')
        
        download_subtitles(video_id)
       
        return render_template("youtube_video.html").format(video_id)
    return render_template("home_page.html")
    
@app.route('/time', methods=['GET', 'POST'])
def time():
    
    if request.method == 'POST':
        start=request.form.get('start')
        end=request.form.get('end')
        
        time_limit(start,end)
        main_matcher()
        ans1,ans2,qu1,qu2=question_answer()
        
        answers.append(ans1)
        answers.append(ans2)
        
        questions.append(qu1)
        questions.append(qu2)

        return render_template("time_limitation.html").format(video_id,start,end)
    return render_template("youtube_video.html").format(video_id) 

@app.route('/question_list',methods=['GET', 'POST'])
def questions_list():
    
    if request.method == 'POST':
        user_answer1=request.form.get('user_answer1')
        user_answer2=request.form.get('user_answer2')
        
        user_answers.append(user_answer1)
        user_answers.append(user_answer2)
        
        return redirect('/time')
    return render_template("questions.html")

@app.route('/finish',methods=['GET', 'POST'])
def finish_exam():
    
    true_count=0
    t = str("""<span style="color:green;font-weight:bold">{}</span>""")
    f = str("""<span style="color:red;font-weight:bold">{}</span>""") + str("""<span style="color:blue;font-weight:bold">{}</span>""")

    with open ("C:\\python\\pydosya\\templates\\result.html","a") as f1:
        
        for i in range(len(answers)):
            if str(answers[i]).lower() == str(user_answers[i]).lower():
            
                true_count+=1               
                true_string = ("<p>" + (str(questions[i]).replace("________", t)).format(answers[i]) + "</p> \n")                
                f1.write("\n{}\n" .format(true_string))
            
            else:

                false_string=("<p>" + (str(questions[i]).replace("________", f)).format(user_answers[i],{answers[i]}) + "</p> \n")                  
                f1.write("\n{}\n".format(false_string))
        
        f1.write(str("End of exam TRUE---------->"   """<span style="color:Lime;font-weight:bold">   {}</span>""").format(true_count))
    
    return render_template("result.html")
    
if __name__ == '__main__':
   app.run(debug=True)  

 