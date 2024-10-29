import pandas as pd
import urllib.request
import ssl, zipfile, os
#from pandas import DataFrame
from dotenv import load_dotenv
load_dotenv()
ENCODING_CSV = os.getenv('ENCODING_CSV')

curr_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = [curr_dir,'datafiles']
base_dir = os.path.join(*save_dir)

def save_kospi_stock_index(base_dir : str = base_dir):
    """
    KOSPI 주식 기초정보를 파일로 다운 받고 DF 로 반환 및 csv 파일로 저장
    Args:
        base_dir (str, optional): Defaults app/util/kospi/datafiles

    Returns:
        DataFrame: 
            column = '단축코드', '표준코드', '한글명', '그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류', '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100', 'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100', 'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC', 'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설', 'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송', 'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지', '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시', '우회상장', '락구분', '액면변경', '증자구분', '증거금비율', '신용가능', '신용기간', '전일거래량', '액면가', '상장일자', '상장주수', '자본금', '결산월', '공모가', '우선주', '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액', '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월', '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
    """
    print('Downloading Kospi')
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/kospi_code.mst.zip",
                                os.path.join(base_dir,"kospi_code.zip"))

    os.chdir(base_dir)
    kospi_zip = zipfile.ZipFile('kospi_code.zip')
    kospi_zip.extractall()
    kospi_zip.close()

    file_name = os.path.join(base_dir,"kospi_code.mst")
    tmp_fil1 = os.path.join(base_dir,"kospi_code_part1.tmp")
    tmp_fil2 = os.path.join(base_dir,"kospi_code_part2.tmp")

    wf1 = open(tmp_fil1, mode="w")
    wf2 = open(tmp_fil2, mode="w")

    with open(file_name, mode="r", encoding="cp949") as f:
        for row in f:
            rf1 = row[0:len(row) - 228]
            rf1_1 = rf1[0:9].rstrip()
            rf1_2 = rf1[9:21].rstrip()
            rf1_3 = rf1[21:].strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
            rf2 = row[-228:]
            wf2.write(rf2)

    wf1.close()
    wf2.close()

    part1_columns = ['단축코드', '표준코드', '한글명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns,  encoding=ENCODING_CSV)

    field_specs = [2, 1, 4, 4, 4,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    1, 9, 5, 5, 1,
                    1, 1, 2, 1, 1,
                    1, 2, 2, 2, 3,
                    1, 3, 12, 12, 8,
                    15, 21, 2, 7, 1,
                    1, 1, 1, 1, 9,
                    9, 9, 5, 9, 8,
                    9, 3, 1, 1, 1
                    ]

    part2_columns = ['그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',
                    '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100',
                    'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100',
                    'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',
                    'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',
                    'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',
                    'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지',
                    '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',
                    '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',
                    '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',
                    '상장주수', '자본금', '결산월', '공모가', '우선주',
                    '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액',
                    '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월',
                    '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
                    ]

    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)

    DF = pd.merge(df1, df2, how='outer', left_index=True, right_index=True) # 데이터 프레임 병합
    DF = DF[(DF['그룹코드'] == 'ST') & (DF['KOSPI'] == 'Y')]    # 필터링. kospi + 주식
    DF.to_csv('kospi_code.csv', index=False)
    # clean temporary file and dataframe
    del (df1)
    del (df2)
    os.remove(tmp_fil1)
    os.remove(tmp_fil2)
    print("Download Done")
    return DF
if __name__ == '__main__':
    save_kospi_stock_index()