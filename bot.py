from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import logging


global username_
getExamPlaces=False
USER, PASS, MARKS = range(3)
#each function will get the result of question asked before its question

#this function will run after user send /start
def start(bot, update):
    #popup these choices
    reply_keyboard = [['Marks', 'Examination Place', 'Other']]
    update.message.reply_text(
        'Hi, my name is ULFDS !. How I can help you?. '
        'Send /cancel to stop talking to me.\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return USER



def user(bot, update):
    #ask the user for for the username and get the result in passw function
    global getExamPlaces
    update.message.reply_text('Please send me the username '
                              ,
                              reply_markup=ReplyKeyboardRemove())
    #if the user needs Examination place and not marks set it to true (Update) (Must move Examination into dependent function
    if update.message.text == "Examination Place":
        getExamPlaces = True
    
    return PASS


def passw(bot, update):
    #ask the user for for the password and get the result in marks function
    update.message.reply_text('Please Send Me Your Password')
    #assign the global variable username_ to the username sent by user
    global username_
    username_ = update.message.text
    return MARKS




def marks(bot, update):
    #assign the  variable password of the user, the bot has asked for password in function passw
    password_=update.message.text
    #get chat id to send the message photo of marks or examination place
    chat_id=update.message.from_user.id
    #get a screen shot for Marks|Exam Places using selenium, it is a python library for web scraping
    getScreenShot(username_,password_)
    
    #send the screen shot that is saved locally
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$

    bot.send_photo(chat_id=chat_id, photo=open('/Users/hasanbadran/Desktop/j.png', 'rb'),timeout=9999*2)
    #end the conv with the user...
    return ConversationHandler.END
    

def getScreenShot(user,passw):
    #load the driver, it can be downloaded "search google for chrome web driver and set its path"
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own path $$$$$$$$$$$$$$$$$$$$$
    driver = webdriver.Chrome("/Users/hasanbadran/Downloads/chromedriver")
    #open the website
    driver.get("http://ulfds1.ul.edu.lb/")
    #find the login html form in website
    username = driver.find_element_by_id("modlgn_username")
    password = driver.find_element_by_id("modlgn_passwd")
    #after we have found them, send the username and password of student
    username.send_keys(user)
    password.send_keys(passw)
    #find the login button
    login_attempt = driver.find_element_by_xpath("//*[@type='submit']")
    #click login
    login_attempt.submit()
    #after being logged in, decide either to get marks or to get exam places according to variable getExamPlaces
    if getExamPlaces == True:
        driver.get('http://ulfds1.ul.edu.lb/index.php?option=com_wrapper&view=wrapper&Itemid=17')
    else:
        driver.get('http://ulfds1.ul.edu.lb/index.php?option=com_wrapper&view=wrapper&Itemid=8')

    #take screen shot and save it locally
    driver.save_screenshot('/Users/hasanbadran/Desktop/j.png')
    #close the chrome driver , we no longer need it ... since we have already saved the photo
    driver.quit()

def cancel(bot, update):
    #get the name of user
    user = update.message.from_user
    #say bye
    update.message.reply_text('Bye'+user.first_name+', ! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    #End the conversation
    return ConversationHandler.END


def main():
    #bot's token.
    #    $$$$$$$$$$$$$$$$$$$$$ change it for your own token $$$$$$$$$$$$$$$$$$$$$
    #    $$$$$$$$$$$$$$$$$$ you can get a token from bot father $$$$$$$$$$$$$$$$$
    updater = Updater("token-here-token-here")

    #register handler to handle the convo
    dp = updater.dispatcher

    #Set the convo logic,entry point is start
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            #if user has sent marks,examination place or other then run function user
            USER: [RegexHandler('^(Marks|Examination Place|Other)$', user)],

            #after function user finished it will return PASS, check it so this function will be fired up after user func ends
            PASS: [MessageHandler(Filters.text, passw),
                   ],
            #after function passw finished it will return value MARKS, "check it" so this function will be fired up after passw func ends
            MARKS: [MessageHandler(Filters.text, marks),
                       ],

        },
         #handle the case when user sends cancel or
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    #add the handler to the dispatcher
    dp.add_handler(conv_handler)
    #start polling message,start waiting for any new message..
    updater.start_polling()
    #set the bot status to idle,ready
    updater.idle()


if __name__ == '__main__':
    main()
