#!/usr/bin/python3
# FBTools by Ashish Chaudhary [http://github.com/yankee101]

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from pyfiglet import Figlet
import selenium.webdriver
import pickle
import sys
import re
import os

class FBTools:

   def __init__(self):
      dcap = dict(DesiredCapabilities.PHANTOMJS)
      dcap["phantomjs.page.settings.userAgent"] = (
          "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
      )    
      serviceArgs = ['--load-images=no',]      
      self.driver=selenium.webdriver.PhantomJS(desired_capabilities=dcap,service_args=serviceArgs)
      

   def login(self):
      print("Provide your credentials for login.")
      print("Credentials are not stored and required only once...")
      email = input("Email/Username/Phone : ")
      password = input("Password : ")
      
      print("Attempting Login...")
      
      self.driver.get("http://m.facebook.com/settings")
      self.driver.find_element_by_name("email").send_keys(email)
      self.driver.find_element_by_name("pass").send_keys(password + Keys.RETURN)

      dummy = 0

      try:
         if self.driver.find_element_by_xpath('//*[@id="header"]/form/table/tbody/tr/td[2]/input').is_displayed() == True:
            print("Successfully logged in. Dumping Cookies...")
            self.cookieDumper()
            print("Dumped Cookies")

      except NoSuchElementException:
            dummy += 1

      if dummy == 1:
         print("xxxxxxx")
         print("Unable to login, try again later.")


   def loginChecker(self):
      if os.path.isfile("cookies.pkl") == True:
         return True
      else:
         return False

   def cookieDumper(self):
      pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))
     

   def cookieInjector(self):
      if os.path.isfile("cookies.pkl") == True:
         cookies = pickle.load(open("cookies.pkl", "rb"))
         self.driver.get("http://m.facebook.com")
         for cookie in cookies:
            self.driver.add_cookie(cookie)
         self.driver.get("http://m.facebook.com/settings")

   def friendWriter(self,friendList):
      if os.path.isfile("friendList.pkl") == True:
         file = open("friendList.pkl",'wb')
      else:
         print("Generating Friend List for the first time.")
         file = open("friendList.pkl",'wb')      
      pickle.dump(friendList,file)


   def friendComparator(self,newList):
      print("Finding who unfriended you! (or you unfriended them)")
      kickingFriends = []
     
      if os.path.isfile("friendList.pkl") == True:
         oldFile = pickle.load(open("friendList.pkl", "rb"))
         for line in oldFile:
            if line.rstrip() not in newList:
               kickingFriends.append(line)
      else:
         print("Failed to find the Old Friend List")
         print("Writing new Friend List")

      self.friendWriter(newList)

      return kickingFriends

   def friendList(self):
      holder = []    
      n = 0
      dummy = 0
      
      print("Fetching Friend List",end='')

      while n <= 500:
         print(".",end='')
         sys.stdout.flush()
         try:
            self.driver.get("https://m.facebook.com/friends/center/friends/?ppk={}".format(n))
            a = 1
            while a<= 10:
               element = self.driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[{}]/table/tbody/tr/td[2]/a'.format(a))
               holder.append(element.text)
               a += 1
            n += 1
         except NoSuchElementException:
            try:
               elem = self.driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[1]/table/tbody/tr/td[2]/a')
               n += 1
            except:
               break

      print("")
      
      return holder

   def notInList(self):
      comparison = self.friendComparator(self.friendList())
      if comparison == []:
         print("xxxxxxx\nNo new Un-friends\nxxxxxxx")
      else:
         print("These prople are no more in your friend list: ")
         print("CAUTION : If they haven't unfriended you, they may have deactivated their account temporarily.")
         print("\nxxxxxxx")
         for kickingFriend in comparison:
            print(kickingFriend)
         print("xxxxxxx")

   def home(self,pageNumber,click):
      if pageNumber == 0 and click == 0:
         self.driver.get("http://m.facebook.com")
      if click == 1:
         try:
            if pageNumber == 1:
               self.driver.find_element_by_xpath('//*[@id="m_newsfeed_stream"]/div[3]/a').click()
            elif pageNumber > 1:
               self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/a').click()
         except NoSuchElementException:
            print("Cannot access the next page.")
            print(self.onPage)
            self.onPage = 0
         
      holder = []
      like_link_holder = []
      comment_link_holder = []
      n = 0
      try:
         while n < 10:
            path = '//*[@id="u_0_{}"]'.format(n)
            post = self.driver.find_element_by_xpath(path)
            if post.text != "":
               comment_package = self.commentExtractor(path)
               if comment_package[0] != False:
                  like_link_holder.append(self.likeExtractor(path))
                  comment_link_holder.append(comment_package[1])
                  holder.append(post.text.strip())
            n += 1
      except NoSuchElementException:
            n += 1
            
      self.returnedList = self.homeParser(holder,like_link_holder,comment_link_holder)
      for index,post in enumerate(self.returnedList[0]):
         print("---{}---\n{}".format(index,self.render(post)))
      print("xxxxxxx")
      self.onPage += 1

   def homeParser(self,posts,like_links,comment_links):
      for post in posts:
         dummy = -1
         for y in posts:
            dummy += 1
            if post != y:
               if y in post:
                  del posts[dummy]
                  del like_links[dummy]
                  del comment_links[dummy]
                  break
      b = -1
      for post in posts:
         b += 1
         if self.isEnglish(post) == False:
            del posts[b]
            del like_links[b]
            del comment_links[b]
            
      return [posts,like_links,comment_links]

   def render(self,post):
      post = re.sub('. Add Friend . Full Story . More','',post)
      post = re.sub('Add Friend\n','',post)
      post = re.sub('. Full Story . More','',post)
      post = re.sub('. Like Page','',post)
      post = re.sub('Like Page . More','',post)
      post = re.sub('. Share','',post)

      return post

   def likeExtractor(self,path):
      try:
         like_link = self.driver.find_element_by_xpath('{}/div[2]/div[2]/div[2]/span[1]/a[2]'.format(path))
         return like_link
      except NoSuchElementException:
         try:
            like_link = self.driver.find_element_by_xpath('{}/div[2]/div[2]/span[1]/a[2]'.format(path))
            return like_link
         except NoSuchElementException:
            return False

   def commentExtractor(self,path):
      try:
         comment_link = self.driver.find_element_by_xpath('{}/div[2]/div[2]/a[1]'.format(path))
         return [True,comment_link]
      except NoSuchElementException:
         return [False,False]

   def like(self,index):
      try:
         self.driver.get(self.returnedList[1][index].get_attribute("href"))
         print("Liked.")
      except:
         print("Unable to like.")

   def comment(self,index):
      try:
         self.driver.get(self.returnedList[2][index].get_attribute("href"))
         comment = input("Enter your comment:\n")
         self.driver.find_element_by_xpath('//*[@id="composerInput"]').send_keys(comment + Keys.RETURN)         
         print("Commented.")
      except:
         print("Unable to comment.")

   def isEnglish(self,s):
      try:
        s.encode('ascii')
      except UnicodeEncodeError:
        return False
      else:
        return True

   def homeActionsParser(self,action):
      operand = -1
      for s in action.split():
         if s.isdigit():
            operand = int(s)
      try:
         if operand == -1:
            print("Invalid command")
            return -1
         elif operand >= len(self.returnedList[1]):
            print("Invalid command")
            return -1
         return operand
      except AttributeError:
         print("Nothing here! So can't perform that action.")
         return -1
         
      
   def greeting(self):
      try:
         if self.driver.find_element_by_xpath('//*[@id="viewport"]/div[3]/div/table/tbody/tr/td[2]/a[3]').is_displayed() == True:
            name = self.driver.find_element_by_xpath('//*[@id="viewport"]/div[3]/div/table/tbody/tr/td[2]/a[3]')
            f = Figlet(font='slant')
            print(f.renderText(re.search('\((.*?)\)',name.text).group(1)))
      except NoSuchElementException:
            pass

   def manager(self,command):
      if command == "help":
         if os.path.isfile("commands.txt"):
            file = open("commands.txt")
            for line in file.readlines():
               print(line)
         else:
            print("Commands list missing.")
      elif command == "exit":
         sys.exit()
      elif command == "unfr":
         self.onPage = 0
         self.notInList()
      elif command == "home":
         self.onPage = 0
         self.home(self.onPage,0)
      elif command == "home next":
         if self.onPage == 0:
            self.home(0,0)
         else:
            self.home(self.onPage,1)
      elif "like" in command != -1:
         operand = self.homeActionsParser(command)
         if operand != -1:
            self.like(operand)
      elif "comment" in command != -1:
         operand = self.homeActionsParser(command)
         if operand != -1:
            self.comment(operand)
      else:
         print("Invalid command. Use 'help' to get a list of commands.")
         
      self.commandInput()

   def commandInput(self):
      print("")
      print("Use 'help' to get the list of commands. Use 'exit' to logoff.")
      command = input("Enter command : ")
      self.manager(command)
 
def main():

   tool = FBTools()
   f = Figlet(font='slant')
   print(f.renderText('FBTools\n------'))
   
   if tool.loginChecker() == True:
      print("Attempting Login...")
      tool.cookieInjector()
   else:
      tool.login()

   tool.greeting()
   tool.commandInput()

if __name__ == "__main__":main()
