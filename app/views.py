from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.models import User 
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from app.models import * 

from IPython.display import Audio
from IPython.utils import io
from pathlib import Path
import numpy as np
import librosa
from app.vocoder import inference as vocoder 
from app.encoder import inference as encoder
from app.synthesizer.inference import Synthesizer
from googletrans import Translator
import wave
#import moviepy.editor
from django.db import models




import pyttsx3
import datetime
import speech_recognition as sr

from .form import Audio_upload
from .form import Ai_bot

encoder_weights = Path("/content/drive/MyDrive/Colab Notebooks/OWL/app/pretrained/encoder/saved_models/pretrained.pt")
vocoder_weights = Path("/content/drive/MyDrive/Colab Notebooks/OWL/app/pretrained/vocoder/saved_models/pretrained/pretrained.pt")
syn_dir = Path("/content/drive/MyDrive/Colab Notebooks/OWL/app/pretrained/synthesizer/saved_models/logs-pretrained/taco_pretrained")
encoder.load_model(encoder_weights)
synthesizer = Synthesizer(syn_dir)
vocoder.load_model(vocoder_weights)

translator = Translator(service_urls=['translate.googleapis.com'])
def Takeinput(Audio):
    r =sr.Recognizer()
    with sr.AudioFile(Audio) as source:
        print("i\'m  listening")
        r.pause_threshold=1
        audio= r.listen(source)
        
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='Ur') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:   
        print("Say that again please...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query


def translate(text):
  result = translator.translate(text, dest='english')
  r1=result.text
  return r1
  


def cloning(text, audio):
  in_fpath = Path(audio)
  reprocessed_wav = encoder.preprocess_wav(in_fpath)
  original_wav, sampling_rate = librosa.load(in_fpath)
  preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
  embed = encoder.embed_utterance(preprocessed_wav)
  with io.capture_output() as captured:
    specs = synthesizer.synthesize_spectrograms([text], [embed])
  generated_wav = vocoder.infer_waveform(specs[0])
  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
  re =Audio(generated_wav, rate=synthesizer.sample_rate)

  with open('/content/drive/MyDrive/Colab Notebooks/OWL/media/bot.wav', 'wb') as f:
    f.write(re.data)

  result ='/content/drive/MyDrive/Colab Notebooks/OWL/media/bot.wav'
  return result


#home page view
@csrf_exempt
def home(request):  
  return render(request,'index.html')
#about us page view
def about(request):
  return render(request,'about.html')

#coctact us page view
@csrf_exempt
def contact(request):
  if request.method == "POST":  
    Name= request.POST['Name']
    LastName= request.POST['LastName']
        
    Email = request.POST['Email']
    Subject= request.POST['Subject']
    Message = request.POST['Message']

    ins=Feedback(Name=Name,LastName=LastName,Email=Email,Subject=Subject,Message=Message)
    ins.save()
    messages.success(request, "your message has been sent, successfuly.")

  return render(request,'contact.html')
#services
def service(request):
  return render(request,'service.html')

## credentials section 
@csrf_exempt
def logins(request):
  if request.method=="POST":
    loginusername=request.POST['Username']
    loginpassword=request.POST['password']

    user=authenticate(username= loginusername, password= loginpassword)
    if user is not None:
      login(request, user)
      return render(request,'index.html')
    else:
      messages.error(request, 'Check your username or password.', extra_tags='safe')
      render(request,'login.html')  
  return render(request,'login.html')

@csrf_exempt
def signUp(request):
  if request.method=="POST":
        # Get the post parameters
        username=request.POST['Username']
        email=request.POST['Email']
        pass1=request.POST['Password']
        pass2=request.POST['con_Password']
        # check for errorneous input
        if (pass1!= pass2):
          messages.error(request, 'Password do not match.', extra_tags='safe')
          return render(request,'signUp.html')
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
       
        return render(request,'login.html')
    
  return render(request,'signUp.html')

#services
@csrf_exempt
def serviceTwo(request):
  
  form = Ai_bot()
  context = {"form": form }
  if request.method == "POST": 
    form = Ai_bot(request.POST, request.FILES)
    user_pr = form.save(commit=False)
    user_pr.text = request.POST['text']
    user_pr.Bot_Sound = request.FILES['Bot_Sound']

    file_type = user_pr.Bot_Sound.url.split('.')[-1]
    file_type = file_type.lower()
    if(file_type =="wav"):
      user_pr.save()

      file_name = user_pr.Bot_Sound.url
      path_f= "/content/drive/MyDrive/Colab Notebooks/OWL"
      full_path =path_f+ file_name
    
      final_audio = cloning(user_pr.text, full_path)
      return render(request,'three_show_audio.html',)
    else:
      messages.error(request,"Make sure your file in right format (wav)")
      return render(request,'serviceTwo.html',context)

  return render(request,'serviceTwo.html',context)

#services
@csrf_exempt
def serviceOne(request):
  if request.method=="POST":
    txt=request.POST['text']
    result = translator.translate(txt, dest='ur')

    return render(request,'serviceOne.html',{'txt': result.text})

  return render(request,'serviceOne.html')

#services
@csrf_exempt
def serviceThree(request):
  form = Audio_upload()
  context = {"form": form,}
  if request.method == "POST": 
    form = Audio_upload(request.POST, request.FILES)
    # if form.is_valid():
    user_pr = form.save(commit=False)
    user_pr.Upload_Audio = request.FILES['Upload_Audio']
    file_type = user_pr.Upload_Audio.url.split('.')[-1]
    file_type = file_type.lower()
    path_f= "/content/drive/MyDrive/Colab Notebooks/OWL"
    if(file_type=="wav"):
      user_pr.save()
      file_name = user_pr.Upload_Audio.url
      full_path =path_f+file_name
      audio_file=user_pr.Upload_Audio

    elif (file_type=="mp4"):
      user_pr.save()
      file_name = user_pr.Upload_Audio.url
      full_path1 =path_f+ file_name

      print(full_path1)
      video = moviepy.editor.VideoFileClip(full_path1)
      audio = video.audio
      
      audio.write_audiofile("/content/drive/MyDrive/Colab Notebooks/OWL/media/converted.wav")
      full_path ="/content/drive/MyDrive/Colab Notebooks/OWL/media/converted.wav"
      audio_file =full_path

    else:
      messages.error(request, 'Make sure your file in mp4 or wav formate.', extra_tags='safe')
      return render(request,'serviceThree.html',context)

    tra=Takeinput(audio_file)
    test=translate(tra)
    
    cloning(test, full_path)
    #user_pr.Upload_Audio=final_audio
    #user_pr.save()
    
    return render(request, 'three_show_audio.html')
  
  return render(request,'serviceThree.html',context)

def Logouts(request):
    logout(request)
    return render(request,'login.html')

### WORKING ON SEPRATE AUDIO FROM VIDEO #####
