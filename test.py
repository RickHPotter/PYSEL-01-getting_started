from selenium import webdriver
import time, requests

import pandas as pd

##################### FUNCTIONS #####################

def search_google(browser, search_query):
    try:
        search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
        image_url = []

        # open browser and begin search
        browser.get(search_url)
        # browser.implicitly_wait(1)
        element = browser.find_element_by_class_name('rg_i')

        # get images source url
        element.click()
        browser.implicitly_wait(1)

        element = browser.find_element_by_class_name('v4dQwb')
        big_img = element.find_element_by_class_name('n3VNCb')
        image_url.append(big_img.get_attribute("src"))

        # unless http it can't be downloaded so avoid them
        if (image_url[0].startswith('http')):

            # download the image and write the name of the product so we can analise
            # what's not adequate and change it manually
            reponse = requests.get(image_url[0])
            if reponse.status_code == 200:
                with open(f"PROD " + search_query + ".jpg","wb") as file:
                    file.write(reponse.content)
                    return image_url
            print('fuck')
        else:
            print(search_query + ' not downloaded')
            return ['oops']
    except:
        print('not written, ' +search_query)
        return ['']

# 00. OPEN EXCEL AND WRITE IT TO A DATAFRAME
excel = 'C:/Scraping/hm/result.xlsx'
data = pd.read_excel(excel, 0)
df = pd.DataFrame(data)


# 01. COPY DATAFRAME DESCRIÇÃO SO THAT WE CAN PASS IT THROUGH 02 AND USE IT TO SEARCH
selected_column = df[['Descrição']]
dfSearch = selected_column.copy()

# 02. REPLACE THE ABRVs SO THAT FINDING IMAGES BECOMES EASIER
# if you include dots, it'll be messy
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('.', ' ') 

dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('ANTITRASP ', 'ANTITRASPARENTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('DESINF ', 'DESINFETANTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('DESC ', 'DESCOLORANTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('TONAL ', 'TONALIZANTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('COND ', 'CONDICIONAR ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('TRAT ', 'TRATAMENTO ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('REMOV ', 'REMOVEDOR ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('HID ', 'HIDRATANTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('PLAST ', 'PLASTICO ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('ANAT ', 'ANATOMICA ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('ABS ', 'ABSORVENTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('Esf ', 'ESFOLIANTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('REP ', 'REPARADOR ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('PROT ', 'PROTETOR ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('CORP ', 'CORPORAL ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('CREM ', 'CREMOSO ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('PER ', 'PEROLADO ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('MASC ', 'MASCARA ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('SHAM ', 'SHAMPOO ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('SAB ', 'SABONETE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('TIT ', 'TITANIUM ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('PREM ', 'PREMIUM ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('LUD ', 'LUDURANA ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('ESM ', 'ESMALTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('LIQ ', 'LIQUIDO ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('ESM ', 'ESMALTE ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('IMP ', 'IMPALA ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('ESC ', 'ESCOVA ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('CR ', 'CREME ')
dfSearch['Descrição'] = dfSearch['Descrição'].str.replace('Cr ', 'CREME ')


# 03. START WEBDRIVER; FOR LOOP TO READ THROUGH EVERY LINE OF OUR DATAFRAME

# INITIALISING BROWSER HERE, OTHERWISE EVERY REQUEST WILL OPEN A NEW CMD AND BROWSER TAB
browser = webdriver.Chrome('C:/Scraping/chromedriver')
browser.set_window_position(0, 0)
browser.set_window_size(500, 400)

for numRow in range(1473, 2360):
    # print(str(numRow) + ' starts')
    # READ DATAFRAME CONTENT AND SEND IT AS SEARCH_QUERY TO DEF SEARCHGOOGLE
    search_query_list = dfSearch.iat[numRow, 0]
    search_query = ''.join(search_query_list)

    print(search_query)
    
    # CALL FOR FUNCTION, GRAB URL BY RETURNING ITS VALUE TO A STRING HERE
    url_list = search_google(browser, search_query)
    url = ''.join(url_list)

    # APPLY CHANGES (irow, icolumn) OF ACTUAL DATAFRAME
    df.iat[numRow, len(df.columns)-1] = url

    # 04. WRITE TO EXCEL
    df.to_excel('result.xlsx', engine='xlsxwriter')
    print(str(numRow) + ' ends\n')
