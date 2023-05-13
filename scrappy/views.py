from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import threading
import io
from django.core.files import File
import time
import csv
from django.core.files.base import ContentFile
from django.contrib import messages
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.shortcuts import get_object_or_404
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from .models import Playlist,Channel
from django.conf import settings
from django.http import HttpResponse, Http404

def register(request):
    return render(request, 'register.html')

def register_data(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
                messages.info(request,'Email Already Exist')
                return redirect('/login/')
        else:
            messages.info(request,'Password not match')
            return redirect("register")
    else:
        return render(request,'register.html')
        # fname = request.POST.get('fname')
        # lname = request.POST.get('lname')
        # email = request.POST.get('email')
        # return render(request,'testing.html')
    # else:
    #     return render(request,'testing.html')
def login(request):
    return render(request, 'login.html')
    
def index(request):
    return render(request, 'index.html')
def blank(request):
    return render(request, 'blank.html')
    
def link_File(request):
    return render(request, 'desc_scrapper.html')

def links(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        file = request.FILES.get('file')
        if not link and not file:
            return render(request, 'testing.html', {'error': 'Please provide a link or upload a file.'})
        elif link and not file:
            scrape(request,link)
            return render(request, 'testing.html')
        elif file and not link:
            df = pd.read_excel(file)
            scrape(request, df)
            return render(request,'testing.html')
        else:
            return render(request,'testing.html')
        ############# End of input form #####################
        
def is_dataframe(data):
    print('checking for dataframe')
    return isinstance(data, pd.DataFrame)
############### checking for dataframe if the file is uploaded?? ################
def download_file(request, file_type, file_id):
    print('File ID:', str(file_id))
    if file_type == 'channel':
        file = get_object_or_404(Channel, id=file_id)
    elif file_type == 'playlist':
        file = get_object_or_404(Playlist, id=file_id)
    else:
        raise Http404('File not found')
    # retrieve the appropriate file model
    # file = get_object_or_404(Channel, id=file_id)
    print('File: ',file)
    # # retrieve the file path from the file model
    file_path = file.file.path
    print('File_Path: ',file_path)
    # # open the file and read its contents
    with open(file_path, 'rb') as f:
        file_contents = f.read()
    
    # # create a Django HTTP response object with the file contents
    response = HttpResponse(file_contents, content_type='application/octet-stream')
    
    # # set the Content-Disposition header so that the file is downloaded
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file.file_name)
    
    return response
####################### Downloading Playlist and Channel files ##################################
def playlist_files(request):
    playlists = Playlist.objects.all()
    files = []
    for playlist in playlists:
        playlist.url = settings.MEDIA_URL + playlist.file.name
        playlist.file_type = 'playlist'
        files.append(playlist)
    context = {
        'files': files
    }
    return render(request, 'file_list.html', context)
################ End of Playlist files into template ###################

def channel_files(request):
    channels = Channel.objects.all()
    files = []
    for channel in channels:
        channel.url = settings.MEDIA_URL + channel.file.name
        channel.file_type = 'channel'
        files.append(channel)
    context = {
        'files': files
    }
    return render(request, 'file_list.html', context)
################ End of Channel files into template ###################

def show_scrapped_data(request):
    channels = Channel.objects.all()
    playlists = Playlist.objects.all()
    files = []
    pfiles = []
    cfiles = []
    for channel in channels:
        channel.url = settings.MEDIA_URL + channel.file.name
        channel.file_type = 'channel'
        files.append(channel)
        cfiles.append(channel)
    for playlist in playlists:
        playlist.url = settings.MEDIA_URL + playlist.file.name
        playlist.file_type = 'playlist'
        files.append(playlist)
        pfiles.append(playlist)
    context = {
        'files': files,
        'pfiles':pfiles,
        'cfiles':cfiles
    }
    return render(request, 'utilities-color.html', context)
    ############### End of All Download File ########################
    
def show_playlist_data(request):
    playlists = Playlist.objects.all()
    pfiles = []
    for playlist in playlists:
        playlist.url = settings.MEDIA_URL + playlist.file.name
        playlist.file_type = 'playlist'
        pfiles.append(playlist)
    context = {
        'files':pfiles,
        'type':"Playlist",
    }
    return render(request, 'utilities-border.html', context)
    ############### End of Playlist Download File ########################
    
def show_channel_data(request):
    channels = Channel.objects.all()
    cfiles = []
    for channel in channels:
        channel.url = settings.MEDIA_URL + channel.file.name
        channel.file_type = 'channel'
        cfiles.append(channel)
    context = {
        'files':cfiles,
        'type':"Channel"
    }
    return render(request, 'utilities-border.html', context)
    ############### End of Channel Download File ########################
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def scrape(request,link):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver_service = webdriver.chrome.service.Service(executable_path=r"E:\FYP\Web_Scrapping\Selenium\webdriver\chromedriver.exe")

    driver = webdriver.Chrome(chrome_options=options, service=driver_service)
    wait = WebDriverWait(driver, 10)
    input_path = link
    
    def process_link(link):
        if "youtube.com/watch" in link: 
            print('Single')
            single_link(link)
        elif "youtube.com/playlist" in link:
            print('Playlist')
            playlist(link)
        elif "youtube.com/" in link and "/playlists" in link and "/@" in link:
                channel_leading_playlists(link)
        elif "youtube.com/@" in link:
            channel(link)
        else:
            print('Nothing is matched')
            ############### End of links calling function #############
            
    def keyword(input_words):
        driver.get("https://www.youtube.com/")
        search = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                            (By.XPATH, '//*[@id="search-input"]/input')))
        search.send_keys(input_words)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                                            (By.XPATH,'//*[@id="search-icon-legacy"]/*[@class="style-scope ytd-searchbox"]')))
        search.submit()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                                            (By.XPATH,"//*[@id='video-title']/yt-formatted-string")))
        user_data = driver.find_elements(By.CSS_SELECTOR, "#title-wrapper > h3>a")
        vlinks = []
        for i in user_data:
                vlinks.append(i.get_attribute('href'))
        print("videos to search length",len(vlinks))
        a = 1
        visited_channels = set()
        wait = WebDriverWait(driver, 10)
        for tag1 in vlinks:
            print("tag ",a," ",tag1)
            driver.get(tag1)
            a=a+1
            channel_name = wait.until(EC.element_to_be_clickable(
                                            (By.XPATH,'//*[@id="owner"]//*[@id="upload-info"]//*[@id="channel-name"]//*[@id="text"]/a'))).text
            channel_href = driver.find_element(By.XPATH,'//*[@id="owner"]//*[@id="upload-info"]//*[@id="channel-name"]//*[@id="text"]/a').get_attribute('href')
        
            if channel_name in visited_channels:
                continue  # skip this video link
            print(channel_name + " href: " +channel_href)
        # Add the channel to our set of visited channels
            visited_channels.add(channel_name)
            process_link(channel_href)
            ################# End of keyword section ################
            
    def extract_links(file_path):
        if os.path.splitext(file_path)[1].lower() == '.xlsx':
            df = pd.read_excel(file_path, sheet_name='Sheet1')
            links = df['Link_tag'].tolist()
        elif os.path.splitext(file_path)[1].lower() == '.csv':
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
            links = df['Link_tag'].tolist()
        else:
            raise ValueError('Invalid file type. Only xlsx and csv files are supported.')
        return links
    ########### End of links extraction function ##########

    def store_csv_data_in_db(file_content, file_name, file_type):
        # Create a new instance of the appropriate model based on file type
        if file_type == 'playlist':
            file_model = Playlist()
        elif file_type == 'channel':
            file_model = Channel()
        else:
            # raise an exception if an invalid file type is provided
            raise ValueError("Invalid file type")

        # Set the file name and save the model
        file_model.file_name = file_name
        file_model.save()

        # Create the file path to save the file to
        file_path = os.path.join(settings.MEDIA_ROOT, 'media', file_type, file_name)
        print('Files pathhhh :'+file_path)

        # Create the file if it does not exist
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                pass

        # Open the file in write mode and write the file content to it
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['v_title', 'v_description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in file_content:
                writer.writerow(row)
            
        # Set the file field on the appropriate model to the file path and save the model
        file_model.file = file_path
        file_model.save()

            ########################

    def channel(link):
        link1 = link+"/playlists"
        channel_data, channel_name = channel_leading_playlists(link1)
        store_csv_data_in_db(channel_data, channel_name,'channel')

    def channel_leading_playlists(link):
        driver.get(link)
        driver.implicitly_wait(10)
        # Get playlist links
        user_data = driver.find_elements(By.CSS_SELECTOR, "#view-more > a")
        mplinks = []
        for i2 in user_data:
            mplinks.append(i2.get_attribute('href'))
        print("Length of Multiple playlist links",len(mplinks))

        # Scrape data for each playlist
        playlist_data = []
        channel_name = driver.find_element(By.CSS_SELECTOR, ".ytd-c4-tabbed-header-renderer yt-formatted-string.ytd-channel-name").text
        channel_name +='.csv'
        for playlists in mplinks:
            playlist_data += playlist(playlists)
        return playlist_data, channel_name

    def playlist(link):
        driver.get(link)
        driver.implicitly_wait(10)

        # Get playlist data
        user_data = driver.find_elements(by=By.CSS_SELECTOR, value='a.ytd-playlist-video-renderer')
        playlist_name = driver.find_element(by=By.XPATH, value='//*[@class="metadata-wrapper style-scope ytd-playlist-header-renderer"]//*[@id="container"]//*[@id="text"]').text
        playlist_name +='.csv'
        plinks = []
        for i3 in user_data:
            plinks.append(i3.get_attribute('href'))
        print("Length of Single playlist links",len(plinks))

        # Scrape data for each video in playlist
        video_data = []
        for x in plinks:
            video_data.append(single_link(x))
        print('Done Everything is done perfectly')
        store_csv_data_in_db(video_data,playlist_name,'playlist')
        return video_data

    def single_link(link):
        driver.get(link)
        wait = WebDriverWait(driver, 10)

        # Get video data
        v_title = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,"h1 yt-formatted-string.ytd-watch-metadata"))).text
        v_click =  wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,".ytd-watch-metadata tp-yt-paper-button#expand"))).click()
        v_description =  wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR,"ytd-text-inline-expander.ytd-watch-metadata"))).text
        return {'v_title': v_title, 'v_description': v_description}
            
    def main(input_path):
        if is_dataframe(input_path):
        # Do something with the DataFrame
            links = input_path['Link_tag']
            for link in links:
                process_link(link)
        elif input_path.startswith('http'):
            process_link(input_path)
        elif input_path:
            keyword(input_path)  
        else:
            print('Invalid input')     
    
# def main(input_path):
#     # check if input is a link or a file path
#     if is_dataframe(input_path):
#         # Do something with the DataFrame
#         links = input_path['Link_tag']
#     else:
#         if is_link(input_path):
#             links = [input_path]
#         else:
#             links = extract_links(input_path)
#     threads = []
#     for link in links:
#         t = threading.Thread(target=process_link, args=(link,))
#         # Launch all threads
#         t.start()
#         threads.append(t)
#     # Wait for all threads to complete
#     for t in threads:
#         t.join()
    # def main(input_path):
    #     # check if input is a link or a file path
        
    #     if is_dataframe(input_path):
    #     # Do something with the DataFrame
    #         links = input_path['Link_tag']
    #         # for link in links:
    #         #     process_link(link)
    #     elif input_path.startswith('http'):
    #         links = input_path
            
    #     # elif input_path:
    #     #     keyword(input_path)  
    #     else:
    #         print('Invalid input') 
            
    #     threads = []
    #     for link in links:
    #             t = threading.Thread(target=process_link, args=(link,))
    #             t.start()
    #             threads.append(t)
    #     for t in threads:
    #             t.join()    
    # input_path = 'python'
    main(input_path)
    return HttpResponse("Scraped Successfully!")