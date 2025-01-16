from selenium import webdriver
#Tarayıcıyı başlatmak ve kontrol etmek için Selenium WebDriver modülünü import eder.
from selenium.webdriver.common.keys import Keys
#Klavye tuşlarını simüle etmek (örneğin, Enter basmak) için Keys sınıfını import eder.
from selenium.common.exceptions import NoSuchElementException, TimeoutException
#Sayfadaki öğe bulunamadığında veya işlem zaman aşımına uğradığında kullanılan hata istisnaları.
from selenium.webdriver.chrome.service import Service as ChromeService
#ChromeDriver'ı başlatmak için gerekli servis sınıfını import eder.
from selenium.webdriver.common.by import By
#Web sayfasındaki öğeleri farklı yöntemlerle (ID, Class, XPath vb.) bulmak için By sınıfını import eder.
from selenium.webdriver.support.ui import WebDriverWait
#Bir öğe veya durum gerçekleşene kadar beklemek için WebDriverWait sınıfını import eder.
from selenium.webdriver.support import expected_conditions as EC
#Beklenen koşulları (örneğin, öğenin tıklanabilir olması) tanımlar.
import time
#Zamanla ilgili işlemler yapmak için time modülünü import eder (örneğin, işlem aralarında beklemek için).


# Giriş yapmak için gerekli olan e-posta ve şifre bilgileri.
HESAP_EPOSTA = "XXXXXXXX"  # LinkedIn giriş e-postanız.
HESAP_SIFRE = "XXXXXXXX"  # LinkedIn giriş şifreniz.
TELEFON = "XXXXXXXX"  # Başvuru sırasında kullanılacak telefon numarası.

# Başvuru işlemini iptal eden fonksiyon.
def basvuru_iptal():
    try:
        kapat_butonu = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        kapat_butonu.click()
        time.sleep(2)
        vazgec_butonu = driver.find_elements(By.CLASS_NAME, "artdeco-modal__confirm-dialog-btn")[1]
        vazgec_butonu.click()
    except NoSuchElementException:
        print("Başvuru iptali için gerekli buton bulunamadı.")

# Elemente güvenli şekilde tıklama fonksiyonu
def guvenli_tikla(element):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", element)
        print("Elemente güvenli şekilde tıklandı.")
    except Exception as e:
        print(f"Elemente tıklanırken hata oluştu: {e}")

# ChromeDriver'ı başlat.
from webdriver_manager.chrome import ChromeDriverManager

chrome_surucu_yolu = ChromeDriverManager().install()

chrome_ayarlar = webdriver.ChromeOptions()
chrome_ayarlar.add_experimental_option("detach", True)
chrome_ayarlar.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlatır.

hizmet = ChromeService(executable_path=chrome_surucu_yolu)
driver = webdriver.Chrome(service=hizmet, options=chrome_ayarlar)

# LinkedIn Giriş Sayfası
driver.get("https://www.linkedin.com")

# Çerezleri reddet.
time.sleep(5)
try:
    reddet_butonu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[action-type="DENY"]')))
    reddet_butonu.click()
except TimeoutException:
    print("Çerez reddetme butonu bulunamadı.")

# Giriş Yap
time.sleep(5)
try:
    giris_yap_butonu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Oturum aç")))
    giris_yap_butonu.click()
except TimeoutException:
    print("Giriş yap butonu bulunamadı.")

time.sleep(2)
try:
    eposta_alani = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    eposta_alani.send_keys(HESAP_EPOSTA)
    sifre_alani = driver.find_element(By.ID, "password")
    sifre_alani.send_keys(HESAP_SIFRE)
    sifre_alani.send_keys(Keys.ENTER)
except TimeoutException:
    print("Giriş formu bulunamadı.")

# İş ilanları sayfasına git
time.sleep(5)
driver.get("https://www.linkedin.com/jobs/search/?keywords=Python%20Geli%C5%9Ftirici")

# Kolay Başvuru filtresini seç
time.sleep(5)
try:
    kolay_basvuru_filtresi = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Kolay Başvuru filtre.']"))
    )
    kolay_basvuru_filtresi.click()
    print("Kolay Başvuru filtresi uygulandı.")
except TimeoutException:
    print("Kolay Başvuru filtresi bulunamadı.")

# Sayfadaki tüm ilanları yükleme ve başvuru yapma
def tum_sayfalari_yukle_ve_basvur():
    while True:
        # Tüm iş ilanlarını yükle
        tum_ilanlari_yukle()

        # Tüm iş ilanlarını al
        tum_ilanlar = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")
        print(f"Bu sayfadaki iş ilanı sayısı: {len(tum_ilanlar)}")

        # İlanlara başvuru yap
        for ilan in tum_ilanlar:
            try:
                print("İlan açılıyor...")
                guvenli_tikla(ilan)
                time.sleep(5)

                # "Kolay Başvur" butonunu bul ve tıkla
                try:
                    kolay_basvur_butonu = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-s-apply button"))
                    )
                    # Buton metnini kontrol etmek için birden fazla yöntem dene
                    buton_metni = kolay_basvur_butonu.get_attribute("innerText").strip().lower()
                    print(f"Bulunan buton metni: {buton_metni}")

                    # Eğer "Uygula" veya "Devam" butonu tespit edilirse ilana başvurmayı atla
                    if buton_metni in ["uygula", "devam"]:
                        print(f"{buton_metni.capitalize()} butonu tespit edildi, ilan atlanıyor.")
                        continue
                    else:
                        print("Kolay Başvur butonu tıklandı.")
                        kolay_basvur_butonu.click()
                except TimeoutException:
                    print("Kolay Başvur butonu bulunamadı, ilan atlanıyor.")
                    continue
                except Exception as e:
                    print(f"Bir hata oluştu: {e}")
                    continue

                # Telefon numarasını gir
                telefon_alani = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[id*=phoneNumber]")))
                telefon_alani.clear()
                telefon_alani.send_keys(TELEFON)

                # İlerleme çubuğunu kontrol et (%50 mi?)
                try:
                    ilerleme_cubugu = driver.find_element(By.CSS_SELECTOR, ".artdeco-completeness-meter__bar")
                    ilerleme_genisligi = ilerleme_cubugu.get_attribute("style")  # style="width: 50%;"
                    if "width: 50%" not in ilerleme_genisligi:
                        print("İlerleme çubuğu %50 değil, başvuru atlanıyor.")
                        basvuru_iptal()
                        continue
                except NoSuchElementException:
                    print("İlerleme çubuğu bulunamadı, başvuru atlanıyor.")
                    basvuru_iptal()
                    continue

                # Son adımda "İncele" butonu var mı kontrol et
                try:
                    incele_butonu = driver.find_element(By.XPATH, "//button[contains(text(), 'İncele')]")
                    print("İncele butonu bulundu, başvuru iptal ediliyor ve bir sonraki ilana geçiliyor.")
                    basvuru_iptal()
                    continue
                except NoSuchElementException:
                    print("İncele butonu bulunamadı, başvuru devam ediyor.")

                # Başvuruyu gönder
                gonder_butonu = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "footer button")))
                if gonder_butonu.get_attribute("data-control-name") == "continue_unify":
                    basvuru_iptal()
                    print("Karmaşık başvuru, atlandı.")
                else:
                    gonder_butonu.click()
                    print("Başvuru başarıyla gönderildi.")

                time.sleep(5)
                kapat_butonu = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
                kapat_butonu.click()

            except NoSuchElementException:
                print("Başvuru düğmesi yok, ilan atlandı.")
                basvuru_iptal()
            except TimeoutException:
                print("Başvuru butonu veya telefon alanı bulunamadı.")



# Sayfayı aşağı kaydırarak tüm ilanları yükleyen fonksiyon
def tum_ilanlari_yukle():
    son_yukseklik = driver.execute_script("return document.body.scrollHeight")
    kaydirma_sayisi = 0
    while kaydirma_sayisi < 2:  # Kaydırma sayısını 2'ye çıkardık
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Sayfa yüklenmesi için bekleme süresi
        yeni_yukseklik = driver.execute_script("return document.body.scrollHeight")

        kaydirma_sayisi += 1
        print(f"{kaydirma_sayisi} kez kaydırma yapıldı.")


# Tüm sayfaları ve ilanları yükle, başvuru yap
print("Tüm ilanlar taranıyor ve başvuru yapılıyor...")
tum_sayfalari_yukle_ve_basvur()

# Tarayıcıyı kapat
print("Tüm işlemler tamamlandı. Tarayıcı kapatılıyor...")
time.sleep(5)
driver.quit()
