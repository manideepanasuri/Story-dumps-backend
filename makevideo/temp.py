import uuid

import requests

from makevideo.helpers import convert_mp3_to_wav, upload_file_to_minio

import textwrap

def split_text(text, max_chars=400):
    return textwrap.wrap(text, max_chars, break_long_words=False)


def func():
    text = '''
    Title: Two times I lost my cool during a job interview. Interested in hearing more stories like that (comment)

    Damn, I feel like we both have the same personality! I'm also a pretty much reserved and calm person unless someone wronged me in some way, and I do have a few stories to share (but might not be as interesting as yours):

    Interview 1

    I interviewed for a telesales position. The introduction part went smoothly. And then we went to the sales part. He asked, can you list a few strategies or ideas to improve sales? So I asked him what kind of products or services are we talking about. He said it could be anything. I told him well, I can't really give you any practical ideas or strategies when I don't even know what kind of products or services are we selling. Then he said something really weird like "All my years working here, I've never encountered any practical ideas anyways." which I don't even understand what he meant. So i tried to explain my perspective, "So what I'm trying to say is that different products and services require different strategies. There isn't a one size fit all solution. For example, you wouldn't ask a twitch streamer to help you promote an IT solution, and fb ads might work better on something like computer peripherals than something like toilet paper." And then he kinda ignored everything i said and asked me again, "So your answer is?" At that point I got fed up and told him, "Nevermind, thanks." and left the online interview before he could say anything.

    Interview 2

    This was for a part-time customer service rep position (Max 20 hours per week, $5 per hour). I actually applied it on January (I've already forgotten about it), and they only reached out to me recently. So I thought they were pretty desperate at that point, and I might get the job. Same as usual, started with the self introduction bla bla bla. Then the interviewer asked why did you apply for this position (She acted as if I was applying for a full-time job), so I just gave some random bs like i'm looking to increase my income aside from my current full time job and to also gain more experience to develop my career bla bla. She even proudly said "Oh, you'd definitely learn a lot of new things in this job! (lmao woman, you think this is some sort of managerial position??) And then she asked if I'm able to commit to this job despite being a part-time job because there's gonna be a lot of work to do. I said yes.

    Things started to get weird here. So she further explained, "Also, you need to make sure to get everything done before you leave work, so you might need to stay back and work overtime sometimes. Are you able to do that?" I said, "Yeah sure, I'll just make sure to get everything done on time." Then she asked, "Are you able to work overtime?" to which I replied, "If i'm getting paid for the extra time, then yes." She then said, "Uhm, actually we're not gonna pay any overtime. But sometimes, you might need to stay back and make sure everything is completed." I started to feel a bit annoyed, but kept my cool and said, "Well if that's the case, I'll just make sure to get things done on time so that I don't need to stay back." Then she said, "Yeah, but sometimes, for example, you reach out to another agent to check on something, and they didn't reply even when your working time is over. So you still need to stay back and follow up with that." I got so pissed off at that point I let out a laugh in a mocking way, and then I said, "Yeah, so I feel like for $5 per hour, that's a bit too much to ask from anyone, don't you think? Have a nice day!" and same as above, left the online interview before she could say anything.

    Interview 3

    Well, this isn't technically an interview, but more of an early screening stage via a phone call. It's for a customer service rep position as well. I thought this was a fully remote position, but then she told me i still need to go to the office once a week. I explained to her that i thought this was a fully remote position, plus I'm disabled, so it's pretty inconvenient for me to commute to work, and asked if she could grant me an exception. I could maybe go there once or twice every month if it's something urgent. She said she'll ask the boss about it later. And then she asked if I could work 16 hours per day for 4 days a week. I said, "But the max number of working hours per week according to the employment law is 45 hours (I'm Asian). That's already more than that." And then she started raising her voice and said in an extremely entitled way, "Not every job is 45 hours only. You need to understand that bla bla bla..." That entitled and condescending tone was what pissed me off. Before she could finish, I interrupted and told her, "You know what, I think this job isn't for me. Thanks." And even when i was saying that, she was still babbling away. But I ended the phone call anyways. After that, the more I think about it, the angrier I got. So i sent a follow up message to her on whatsapp (a common way to communicate here), I told her the employment act specifically said the max is 45 hours, 16 x 4 that's already 64 hours. You sound like it's morally wrong to want a work-life balance. People are humans too. We have our lives to live too. Not everyone is entitled to be your corporate slave. I withdraw my application, good luck in finding a suitable candidate. And then i blocked her.


    I used to be like no matter how ridiculous or entitled the interviewer is, I'll just say yes to everything thinking that would land me the job. Years of working experience told me the otherwise. So nowadays, I don't deal with their bs anymore.
    '''
    url = "http://localhost:8880/v1/audio/speech"
    chunks = split_text(text, max_chars=400)
    final_audio = b""
    print(len(chunks))
    count = 0
    for chunk in chunks:
        payload = {
            "input": chunk,
            "voice": "af_alloy",
            "response_format": "mp3",
            "download_format": "mp3",
            "stream": True,
            "speed": 1,
            "return_download_link": True
        }
        response = requests.post(url, json=payload, stream=True)
        print(response.status_code)
        print(count)
        if response.status_code == 200:
            file_bytes = response.content
            final_audio += file_bytes
            print("hello")
        count += 1
    file_bytes = convert_mp3_to_wav(final_audio)
    filename = f"{uuid.uuid4()}.wav"
    fileurl = upload_file_to_minio(file_bytes, filename)
    print(fileurl)


