css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://media.licdn.com/dms/image/D4D03AQHPFh1wWvpvvQ/profile-displayphoto-shrink_800_800/0/1699023873107?e=2147483647&v=beta&t=k5O-oPj0Lp7Uv--r9e_ZiK5CTQqVYd09eyqvcQukc6A" >
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjTXKHVV278pctgx_q_5ywF9lUr5-lfdMDQG5FlNSICM7kGUxuB_V9jOaxOOEt7sbYlMXXe1u2gkoRcAPnOrbX9UWCKvNKOqrjlhHi8cuj4BqWHhvGW2z1VL2ws74C_-_8ylyyjqW3uQKVQ/s2000/Ana+de+Armas.jpg">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
