from __future__ import annotations
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
EDU = ROOT.parent / 'EDU'

SOURCES = {
    'kanoon81': ('قلم‌چی، آزمون ۱۸ مهر ۱۳۹۹، یازدهم تجربی، سؤال ۸۱', 'refs/kanoon.pdf', 1),
    'kanoon82': ('قلم‌چی، آزمون ۱۸ مهر ۱۳۹۹، یازدهم تجربی، سؤال ۸۲', 'refs/kanoon.pdf', 1),
    'k1402q18': ('کنکور ریاضی ۱۴۰۲، نوبت دوم، دفترچهٔ اول، سؤال ۱۸', '../EDU/math/source/pdfs/Kounkor_AI/1402/سوالات کنکور ریاضی 1402 - دفترچه اول - نوبت دوم.pdf', 5),
    'k1402q20': ('کنکور ریاضی ۱۴۰۲، نوبت دوم، دفترچهٔ اول، سؤال ۱۸', '../EDU/math/source/pdfs/Kounkor_AI/1402/سوالات کنکور ریاضی 1402 - دفترچه اول - نوبت دوم.pdf', 5),
    'k1402q30': ('کنکور ریاضی ۱۴۰۵، دفترچهٔ اول، سؤال ۳۰', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور ریاضی 1405 - دفترچه اول.pdf', 7),
    'k1402q34': ('کنکور ریاضی ۱۴۰۲، نوبت دوم، دفترچهٔ اول، سؤال ۳۴', '../EDU/math/source/pdfs/Kounkor_AI/1402/سوالات کنکور ریاضی 1402 - دفترچه اول - نوبت دوم.pdf', 7),
    'k1402q36': ('کنکور ریاضی ۱۴۰۲، نوبت دوم، دفترچهٔ اول، سؤال ۳۶', '../EDU/math/source/pdfs/Kounkor_AI/1402/سوالات کنکور ریاضی 1402 - دفترچه اول - نوبت دوم.pdf', 8),
    'k1403q111': ('کنکور تجربی ۱۴۰۳، نوبت اول، دفترچهٔ سوم، سؤال ۱۱۱', '../EDU/math/source/pdfs/Kounkor_AI/1403/سوالات کنکور تجربی 1403 - دفترچه سوم - نوبت اول.pdf', 2),
    'k1403q113': ('کنکور تجربی ۱۴۰۳، نوبت اول، دفترچهٔ سوم، سؤال ۱۱۳', '../EDU/math/source/pdfs/Kounkor_AI/1403/سوالات کنکور تجربی 1403 - دفترچه سوم - نوبت اول.pdf', 2),
    'k1403q140': ('کنکور تجربی ۱۴۰۳، نوبت اول، دفترچهٔ سوم، سؤال ۱۴۰', '../EDU/math/source/pdfs/Kounkor_AI/1403/سوالات کنکور تجربی 1403 - دفترچه سوم - نوبت اول.pdf', 5),
    'k1404q35': ('کنکور ریاضی ۱۴۰۴، نوبت اول، دفترچهٔ اول، سؤال ۳۵', '../EDU/math/source/pdfs/Kounkor_AI/1404/سوالات کنکور ریاضی 1404 - دفترچه اول - نوبت اول.pdf', 7),
    'k1404q36': ('کنکور ریاضی ۱۴۰۴، نوبت اول، دفترچهٔ اول، سؤال ۳۶', '../EDU/math/source/pdfs/Kounkor_AI/1404/سوالات کنکور ریاضی 1404 - دفترچه اول - نوبت اول.pdf', 8),
    'k1405q22': ('کنکور ریاضی ۱۴۰۵، دفترچهٔ اول، سؤال ۲۲', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور ریاضی 1405 - دفترچه اول.pdf', 5),
    'k1405q30': ('کنکور ریاضی ۱۴۰۵، دفترچهٔ اول، سؤال ۳۰', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور ریاضی 1405 - دفترچه اول.pdf', 7),
    'k1405q34': ('کنکور ریاضی ۱۴۰۵، دفترچهٔ اول، سؤال ۳۴', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور ریاضی 1405 - دفترچه اول.pdf', 7),
    'k1405q35': ('کنکور ریاضی ۱۴۰۵، دفترچهٔ اول، سؤال ۳۵', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور ریاضی 1405 - دفترچه اول.pdf', 8),
    'k1405q135': ('کنکور تجربی ۱۴۰۵، دفترچهٔ دوم، سؤال ۱۳۵', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور تجربی 1405 - دفترچه دوم.pdf', 6),
    'k1405q136': ('کنکور تجربی ۱۴۰۵، دفترچهٔ دوم، سؤال ۱۳۶', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور تجربی 1405 - دفترچه دوم.pdf', 6),
    'k1399math22': ('کنکور ریاضی ۱۴۰۲، نوبت دوم، دفترچهٔ اول، سؤال ۱۸', '../EDU/math/source/pdfs/Kounkor_AI/1402/سوالات کنکور ریاضی 1402 - دفترچه اول - نوبت دوم.pdf', 5),
    'k1399circle': ('کنکور ریاضی ۱۴۰۵، دفترچهٔ اول، سؤال ۳۴', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور ریاضی 1405 - دفترچه اول.pdf', 7),
    'k1399ellipse': ('کنکور ریاضی ۱۴۰۴، نوبت اول، دفترچهٔ اول، سؤال ۳۶', '../EDU/math/source/pdfs/Kounkor_AI/1404/سوالات کنکور ریاضی 1404 - دفترچه اول - نوبت اول.pdf', 8),
    'k1401ellipse': ('کنکور تجربی ۱۴۰۵، دفترچهٔ دوم، سؤال ۱۳۵', '../EDU/math/source/pdfs/Kounkor_AI/1405/سوالات کنکور تجربی 1405 - دفترچه دوم.pdf', 6),
}

# The related-practice links use these small, content-specific skill labels.
OLD_TAGS = {
 1:['slope','two-points'],2:['vertical-line','intercept'],3:['slope','intercept'],4:['perpendicular','intercept'],5:['parallel'],6:['intercepts','area'],7:['line-equation','two-points'],8:['perpendicular','line-equation'],9:['intercepts','area'],10:['intercepts','parameter'],
 11:['distance','horizontal'],12:['midpoint'],13:['reflection','midpoint'],14:['equal-distance','coordinates'],15:['parallelogram','midpoint'],16:['minimization','distance'],17:['reflection','midpoint'],18:['altitude','median','distance'],19:['parallelogram','center'],20:['shortest-path','reflection'],
 21:['point-line-distance'],22:['point-line-distance','origin'],23:['point-on-line'],24:['parallel-lines','distance'],25:['area','point-line-distance'],26:['parallel-lines','distance'],27:['point-line-distance','origin'],28:['altitude','point-line-distance'],29:['center-side-distance','area'],30:['parallel-lines','distance'],
 31:['vertex'],32:['axis'],33:['vertex','roots'],34:['maximum','vertex'],35:['vertex','coefficient'],36:['roots','intercept'],37:['intersection','distance'],38:['tangent','vertex'],39:['tangent','intersection'],40:['vertex','parameter'],
 41:['focal-sum'],42:['foci','center'],43:['axes','foci'],44:['eccentricity','axes'],45:['focal-sum','foci'],46:['eccentricity','foci'],47:['focal-distance','axes'],48:['eccentricity','foci'],49:['area','axes'],50:['eccentricity','focal-ratio'],
 51:['circle-center'],52:['circle-radius'],53:['circle-radius','equation'],54:['circle-chord','distance'],55:['circle-tangent','count'],56:['circle-tangent','intercept'],57:['circle-center','diameter'],58:['circle-tangent','tangent-length'],59:['circle-chord','distance'],60:['circle-chord','line'],
 61:['circle-intersections','position'],62:['circle-intersections','internal-tangent'],63:['circle-intersections','concentric'],64:['circle-intersections','integer-count'],65:['distance-between-circles'],66:['common-chord'],67:['circle-intersections','triangle'],68:['common-chord','equations'],69:['common-chord','foci'],70:['common-chord','equations']
}

OLD_SHORTCUTS = {
 7:'از عرض ۲ روی [[y=2x-2]]، طول نقطه را یک‌بار به دست می‌آوریم و سپس شیب خط را از همان نقطه و برخورد معلوم حساب می‌کنیم.',
 8:'شیب خط داده‌شده [[-1/2]] است؛ شیب عمود [[2]] می‌شود و با جای‌گذاری گزینه‌ها، نقطهٔ سازگار فوراً مشخص می‌شود.',
 9:'برای مساحت، قاعده روی محور افقی است؛ پس ارتفاع فقط عرض نقطهٔ برخورد دو خط است، نه طول عمود روی خط مورب.',
 17:"وسط [[BC]] را مستقیم حساب می‌کنیم؛ قرینهٔ [[A]] نسبت به آن مرکز با رابطهٔ [[A'=2M-A]] به دست می‌آید.",
 18:'چون [[BC]] افقی است، پای ارتفاع و پای میانه هر دو روی همان ضلع‌اند؛ کافی است طول‌هایشان را روی محور مقایسه کنیم.',
 19:'مرکز هر متوازی‌الاضلاع، وسط یک جفت رأس مقابل است؛ سه جفت ممکن را بررسی می‌کنیم و نقطهٔ ناممکن را حذف می‌کنیم.',
 27:'از دو نقطه معادلهٔ خط را می‌سازیم و فاصلهٔ مبدأ را با قدرمطلق ثابت تقسیم بر [[√(a^2+b^2)]] می‌یابیم.',
 28:'ارتفاع مثلث همان فاصلهٔ رأس [[C]] از خط [[AB]] است؛ فرمول فاصلهٔ نقطه از خط از پیدا کردن پای ارتفاع سریع‌تر است.',
 29:'فاصلهٔ مرکز مربع از ضلع نصف طول ضلع است؛ پس پس از محاسبهٔ فاصله، آن را دو برابر می‌کنیم و مربع می‌گیریم.',
 57:'مرکز روی خطِ حامل قطر قرار دارد و از دو نقطهٔ داده‌شده فاصلهٔ برابر دارد؛ این دو شرط یک دستگاه خطی ساده می‌سازند.'
}

STEM_ENDINGS = {
 1:('شیب چند است؟','شیب این خط چه مقداری است؟'),
 3:('چیست؟','چه مقداری است؟'),
 6:('چیست؟','چه مقداری است؟'),
 9:('مساحت مثلث؟','مساحت مثلثِ ساخته‌شده چه مقداری است؟'),
 10:('چیست؟','کدام است؟'),
 11:('چند است؟','چند واحد است؟'),
 12:('چه عرضی دارد؟','عرض نقطهٔ میانی چه مقداری است؟'),
 13:('چه طولی دارد؟','طول مختصات قرینه کدام است؟'),
 14:('عرضش چیست؟','عرض این نقطه چه مقداری است؟'),
 15:('عرض رأس چهارم چیست؟','عرض مختصات رأس چهارم کدام است؟'),
 16:('مقدار کمینه چیست؟','کمترین مقدار مجموع مجذور فاصله‌ها کدام است؟'),
 23:('چیست؟','چه مقداری است؟'),
 25:('مساحت؟','مساحت مثلث کدام است؟'),
 26:('فاصلهٔ دو دارند؟','فاصلهٔ دو واحد دارند؟'),
 29:('مساحت مربع؟','مساحت این مربع چه مقداری است؟'),
 30:('چند است؟','چه مقداری است؟'),
 31:('چه عرضی دارد؟','عرض مختصات رأس سهمی کدام است؟'),
 32:('چه طولی دارد؟','محور تقارن سهمی کدام خط است؟'),
 33:('طول رأس؟','طول مختصات رأس سهمی کدام است؟'),
 34:('چقدر است؟','بیشترین ارتفاع مسیر چه مقداری است؟'),
 35:('ضریب درجهٔ دو؟','ضریب درجهٔ دوِ سهمی کدام است؟'),
 36:('عرض از مبدأ؟','عرض از مبدأ سهمی چه مقداری است؟'),
 37:('فاصلهٔ این دو نقطه؟','فاصلهٔ دو نقطهٔ برخورد چند واحد است؟'),
 38:('چیست؟','چه مقداری است؟'),
 39:('طول آن نقطه چیست؟','طول مختصات نقطهٔ تماس کدام است؟'),
 40:('چقدر است؟','فاصلهٔ دو رأس متناظر چه مقداری است؟'),
 41:('مجموع فاصله‌ها از دو کانون؟','مجموع فاصله‌های یک نقطهٔ بیضی تا دو کانون کدام است؟'),
 42:('طول مرکز؟','طول مختصات مرکز بیضی کدام است؟'),
 43:('فاصلهٔ کانون‌ها؟','فاصلهٔ دو کانون بیضی چه مقداری است؟'),
 44:('قطر کوچک؟','طول قطر کوچک بیضی کدام است؟'),
 45:('نیم‌قطر کوچک؟','نیم‌قطر کوچک بیضی چه مقداری است؟'),
 46:('خروج از مرکز؟','خروج از مرکز بیضی کدام است؟'),
 47:('فاصلهٔ سر قطر کوچک از مرکز؟','فاصلهٔ سرِ قطر کوچک از مرکز بیضی چند واحد است؟'),
 48:('خروج از مرکز؟','خروج از مرکز بیضی چه مقداری است؟'),
 49:('چقدر است؟','مساحت بیشینهٔ این مثلث چه مقداری است؟'),
 51:('چه عرضی دارد؟','عرض مختصات مرکز دایره چه مقداری است؟'),
 52:('شعاع؟','شعاع دایره چه مقداری است؟'),
 53:('چیست؟','چه مقداری است؟'),
 54:('چه وتری جدا می‌کند؟','طول وتری که این خط از دایره جدا می‌کند چند واحد است؟'),
 56:('چه عرض از مبدأیی دارد؟','عرض از مبدأ خط مماس چه مقداری است؟'),
 57:('شعاع؟','شعاع این دایره کدام است؟'),
 58:('طول پاره‌خط مماس؟','طول پاره‌خط مماس چه مقداری است؟'),
 59:('فاصلهٔ خط‌های حامل آن‌ها؟','فاصلهٔ دو خط حامل این وترها چند واحد است؟'),
 60:('چیست؟','کدام است؟'),
 61:('چند نقطهٔ مشترک دارند؟','تعداد نقاط مشترک این دو دایره کدام است؟'),
 62:('فاصلهٔ مرکزها؟','فاصلهٔ دو مرکز چه مقداری است؟'),
 65:('کمترین فاصلهٔ دو محیط؟','کمترین فاصلهٔ بین دو محیط چند واحد است؟'),
 66:('چه طولی دارد؟','طول وتر مشترک این دو دایره کدام است؟'),
 68:('طول وتر مشترک؟','طول وتر مشترک این دو دایره چه مقداری است؟'),
 69:('فاصلهٔ مرکزها چیست؟','فاصلهٔ مرکزهای این دو دایره چه مقداری است؟'),
 70:('شعاع اول چیست؟','شعاع دایرهٔ اول چه مقداری است؟')
}


def fa_digits(s: str) -> str:
    return str(s).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))

def math_html(s: str) -> str:
    def render(m):
        value=style_math_html(html.escape(m.group(1)))
        return '<bdi class="math" dir="ltr">'+value+'</bdi>'
    return re.sub(r'\[\[(.*?)\]\]', render, s)

def style_math_html(value: str) -> str:
    superscripts=str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾','0123456789+-=()')
    subscripts=str.maketrans('₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎','0123456789+-=()')
    value=re.sub(r'\$([^$]+)\$',r'\1',value)
    value=re.sub(r'\^\{([^{}]+)\}',r'<sup>\1</sup>',value)
    value=re.sub(r'\^(-?\d+|[A-Za-z])',r'<sup>\1</sup>',value)
    value=re.sub(r'_\{([^{}]+)\}',r'<sub>\1</sub>',value)
    value=re.sub(r'_([A-Za-z0-9]+)',r'<sub>\1</sub>',value)
    value=re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾]+',lambda x:'<sup>'+x.group().translate(superscripts)+'</sup>',value)
    value=re.sub(r'[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎]+',lambda x:'<sub>'+x.group().translate(subscripts)+'</sub>',value)
    return value

def math_tex(s: str) -> str:
    def render(m):
        value=m.group(1)
        if value.startswith('$') and value.endswith('$'): value=value[1:-1]
        return r'\lr{$'+value+'$}'
    return re.sub(r'\[\[(.*?)\]\]', render, s)

def math_style_tex(s: str) -> str:
    out=[]; pos=0
    while True:
        start=s.find(r'\lr{',pos)
        if start<0:
            out.append(s[pos:]); break
        out.append(s[pos:start])
        i=start+4; depth=1
        while i<len(s) and depth:
            if s[i]=='{': depth+=1
            elif s[i]=='}': depth-=1
            i+=1
        if depth:
            out.append(s[start:]); break
        value=s[start+4:i-1]
        if not (value.startswith('$') and value.endswith('$')):
            value='$'+value+'$'
        out.append(r'\lr{'+value+'}')
        pos=i
    return ''.join(out)

def is_math_option(s: str) -> bool:
    return bool(re.fullmatch(r'[A-Za-z0-9۰-۹٠-٩۰-۹+\-−√/().,=^_ ]+',s))

def option_html(s: str) -> str:
    return math_html('[['+s+']]') if is_math_option(s) else html.escape(s)

def option_tex(s: str) -> str:
    if not is_math_option(s): return s
    if s.startswith('$') and s.endswith('$'): s=s[1:-1]
    return r'\lr{$'+s+'$}'

def polish_language(s: str) -> str:
    pairs = [
      ('شروع و پایان حرکت را مشخص کن','ابتدا نقطهٔ آغاز و پایان حرکت را مشخص می‌کنیم'),
      ('چک کن','بررسی می‌کنیم'),('چک کنیم','بررسی می‌کنیم'),('حساب کن','محاسبه می‌کنیم'),
      ('فرض کن','فرض می‌کنیم'),('در نظر بگیر','در نظر می‌گیریم'),('بگیر','در نظر می‌گیریم'),
      ('بگذار','قرار می‌دهیم'),('بگذارید','قرار می‌دهیم'),('بنویس','می‌نویسیم'),
      ('بیرون بکش','به دست می‌آوریم'),('پیدا کن','به دست می‌آوریم'),('حذف کن','حذف می‌کنیم'),
      ('کم کن','از دو طرف کم می‌کنیم'),('به سمت راست ببر','به سمت راست می‌بریم'),
      ('به هم وصل کن','به هم وصل می‌کنیم'),('یک بار دیگر ادامه بده','یک بار دیگر ادامه می‌دهیم'),
      ('می‌توانی','می‌توانیم'),('کدام جواب را برمی‌داری','کدام گزینه به دست می‌آید')]
    for a,b in pairs: s=s.replace(a,b)
    return s

def related_block(qid: int, items_by_id: dict[int,dict], related_ids: list[int], html_stems: dict[int,str], answers: dict[int,int]) -> str:
    rows=[]
    for rid in related_ids:
        short=html_stems[rid]
        rows.append(f'<li><a href="#q{rid}">تست {fa_digits(rid)}: {short}</a></li>')
    return '<details class="related" id="related-q'+str(qid)+'"><summary>۵ تمرین مرتبط با این سؤال</summary><ul>'+''.join(rows)+'</ul></details>'

def make_new_article(q: dict) -> str:
    source=q['source']; file=quote(q['source_file'],safe='/')
    opts='　'.join(f'{fa_digits(i+1)}) {option_html(v)}' for i,v in enumerate(q['choices']))
    return (f'<article id="q{q["id"]}"><small>تست {fa_digits(q["id"])} · بازنویسی با تغییر داده‌ها</small> '
      f'<a class="source" href="{file}#page={q["source_page"]}">منبعِ الگو: {html.escape(source)}</a>'
      f'<p><b>{math_html(q["stem"])}</b></p><div class="opts">{opts}</div>'
      f'<details class="answer answer-reveal"><summary>پاسخ نهایی</summary><p>گزینهٔ {fa_digits(q["answer"])}</p></details>'
      f'<details id="solution-q{q["id"]}"><summary>حل تشریحی</summary><p>{math_html(q["solution"])}</p></details>'
      f'<details class="shortcut"><summary><b>راه سریع</b></summary><p>{math_html(q["shortcut"])}</p></details>'
      f'__RELATED_{q["id"]}__</article>')


def main():
    tex_path=ROOT/'booklet.tex'; html_path=ROOT/'index.html'
    tex=tex_path.read_text(); page=html_path.read_text()
    preamble=(r'\documentclass[11pt,a4paper]{article}'+'\n'
      +r'\usepackage[margin=22mm]{geometry}'+'\n'
      +r'\usepackage{tikz}'+'\n'
      +r'\usepackage{xepersian}'+'\n'
      +r'\settextfont[Path=fonts/,BoldFont={XB NiloofarBd.ttf}]{XB Niloofar.ttf}'+'\n'
      +r'\setlatintextfont[Path=fonts/]{Math.ttf}'+'\n'
      +r'\usepackage{unicode-math}'+'\n'
      +r'\setmathfont{STIX Two Math}'+'\n'
      +r'\setlength{\parskip}{6pt}'+'\n'
      +r'\linespread{1.08}'+'\n'
      +r'\begin{document}'+'\n')
    tex=re.sub(r'\\documentclass[^\n]*\n(?:.*\n)*?\\begin\{document\}\n',lambda _:preamble,tex,count=1)
    raw=[json.loads(line) for line in (ROOT/'supplement.jsonl').read_text().splitlines() if line.strip()]
    for q in raw:
        label,file,pn=SOURCES[q['source_key']]
        q['source']='تمرین بازنویسی‌شده با تغییر داده‌ها، بر پایهٔ '+label
        q['source_file']=file; q['source_page']=pn
    (ROOT/'supplement.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')
    # Polish existing short question endings in both output formats.
    for qid,(old,new) in STEM_ENDINGS.items():
        # apply to the question text only in HTML
        pattern=re.compile(r'(<article id="q'+str(qid)+r'">.*?<p><b>)(.*?)(</b></p>)',re.S)
        m=pattern.search(page)
        if m:
            stem=m.group(2)
            if stem.endswith(old): page=page[:m.start(2)]+stem[:-len(old)]+new+page[m.end(2):]
        # Rewrite only the prompt for this numbered test in TeX.
        qpat=re.compile(r'(\\paragraph\{تست\s+'+str(qid)+r'\}.*?\\par)(.*?)(\\par)',re.S)
        tm=qpat.search(tex)
        if tm and tm.group(2).endswith(old):
            tex=tex[:tm.start(2)]+tm.group(2)[:-len(old)]+new+tex[tm.end(2):]
    # Smooth imperative phrasing without changing the mathematics.
    page=polish_language(page); tex=polish_language(tex)
    # Old-source fast hints and answer labels in the HTML.
    old_article_data={}; old_solutions={}
    for qid in range(1,71):
        m=re.search(r'<article id="q'+str(qid)+r'">(.*?)</article>',page,re.S)
        if not m: raise RuntimeError(f'old HTML article {qid} not found')
        body=m.group(1)
        stem_m=re.search(r'<p><b>(.*?)</b></p>',body,re.S)
        if not stem_m: continue
        stem_html=stem_m.group(1); stem_text=html.unescape(re.sub(r'<[^>]+>','',stem_html))
        sol_m=re.search(r'<details[^>]*>\s*<summary>حل تشریحی</summary>\s*<p>(.*?)</p>',body,re.S)
        sol=sol_m.group(1) if sol_m else ''
        ans_m=re.search(r'گزینهٔ?\s*([0-9۰-۹٠-٩]+)',html.unescape(re.sub(r'<[^>]+>','',sol)))
        if not ans_m:
            # Answer keys are also present in the TeX solution headings.
            tm=re.search(r'\\paragraph\{تست\s+'+str(qid)+r'؛\s*گزینهٔ?\s*([0-9۰-۹٠-٩]+)',tex)
            if tm: ans_m=tm
        ans=int(ans_m.group(1).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩','01234567890123456789'))) if ans_m else 0
        tags=OLD_TAGS.get(qid,['lesson-'+str((qid-1)//10+1)])
        old_article_data[qid]={'id':qid,'lesson':(qid-1)//10+1,'tags':tags,'stem_html':stem_html,'stem_text':stem_text,'answer':ans,'source':bool(re.search(r'بازنویسی|قلم.?چی|کنکور',body))}
        old_solutions[qid]=sol
        # Add a visible answer badge, and an addressable solution for the practice links.
        if ans and '<p class="answer">' not in body and 'class="answer answer-reveal"' not in body:
            body=body.replace('<details><summary>حل تشریحی</summary>',f'<details class="answer answer-reveal"><summary>پاسخ نهایی</summary><p>گزینهٔ {fa_digits(ans)}</p></details><details id="solution-q{qid}"><summary>حل تشریحی</summary>',1)
        elif '<details><summary>حل تشریحی</summary>' in body:
            body=body.replace('<details><summary>حل تشریحی</summary>',f'<details id="solution-q{qid}"><summary>حل تشریحی</summary>',1)
        body=re.sub(r'<p class="answer">پاسخ نهایی: گزینهٔ\s*([۰-۹0-9]+)</p>',r'<details class="answer answer-reveal"><summary>پاسخ نهایی</summary><p>گزینهٔ \1</p></details>',body)
        body=re.sub(r'<span class="answer">پاسخ گزینهٔ\s*([۰-۹0-9]+)</span>',r'<details class="answer answer-reveal related-answer"><summary>پاسخ</summary><span>گزینهٔ \1</span></details>',body)
        # Keep explanations in connected, explanatory first-person prose.
        for a,b in [('پیدا کن','به دست می‌آوریم'),('بگیر','در نظر می‌گیریم'),('بگذار','قرار می‌دهیم'),('بنویس','می‌نویسیم'),('کم کن','از دو طرف کم می‌کنیم'),('چک کن','بررسی می‌کنیم'),('فرض کن','فرض می‌کنیم'),('حساب کن','محاسبه می‌کنیم')]: body=body.replace(a,b)
        if qid in OLD_SHORTCUTS and '<details class="shortcut">' not in body:
            tip=f'<details class="shortcut"><summary><b>راه سریع</b></summary><p>{math_html(OLD_SHORTCUTS[qid])}</p></details>'
            body=re.sub(r'(<details class="related"[^>]*><summary>۵ تمرین مرتبط.*?</ul></details>)',tip+r'\1',body,count=1,flags=re.S)
        page=page[:m.start(1)]+body+page[m.end(1):]
    # Add the 70 supplemental question records to their matching lemma sections.
    new_by_lesson={i:[] for i in range(1,8)}
    for q in raw: new_by_lesson[q['lesson']].append(q)
    for lesson,qs in new_by_lesson.items():
        marker=re.compile(r'(<section><h2>لم\s+'+fa_digits(lesson)+r'(?=[\sـ]).*?</section>)',re.S)
        m=marker.search(page)
        if not m: raise RuntimeError(f'HTML section {lesson} not found')
        section=m.group(1); inserted=''.join(make_new_article(q) for q in qs)
        section=section.replace('</section>',inserted+'</section>')
        page=page[:m.start(1)]+section+page[m.end(1):]
    # Combine old and new items for individualized related-practice recommendations.
    all_items={}
    html_stems={}; answers={}
    for qid,d in old_article_data.items():
        all_items[qid]=d; html_stems[qid]=d['stem_html']; answers[qid]=d['answer']
    for q in raw:
        d=dict(q); d['stem_html']=math_html(q['stem']); all_items[q['id']]=d
        html_stems[q['id']]=d['stem_html']; answers[q['id']]=q['answer']
    def choose_related(qid):
        q=all_items[qid]
        candidates=[v for v in all_items.values() if v['lesson']==q['lesson'] and v['id']!=qid]
        scored=[]
        for v in candidates:
            overlap=len(set(q.get('tags',[])) & set(v.get('tags',[])))
            scored.append((overlap,v['id'],v))
        matched=sorted((x for x in scored if x[0]>0),key=lambda x:(-x[0],x[1]))
        broader=sorted((x for x in scored if x[0]==0),key=lambda x:x[1])
        # Start with matching skills; extend within the same lesson if fewer than five exist.
        pool=matched if len(matched)>=5 else matched+broader
        n=len(pool); offset=(qid*3)%n; result=[]
        for k in range(n):
            v=pool[(offset+k)%n][2]
            if v['id'] not in [x['id'] for x in result]: result.append(v)
            if len(result)==5: break
        return [x['id'] for x in result]
    rels={qid:choose_related(qid) for qid in all_items}
    # Replace each old repeated five-question list, then fill new article placeholders.
    for qid in range(1,71):
        block=related_block(qid,all_items,rels[qid],html_stems,answers)
        pattern=re.compile(r'(<article id="q'+str(qid)+r'">.*?)(<details class="related"[^>]*><summary>۵ تمرین مرتبط.*?</ul></details>)(.*?</article>)',re.S)
        page,n=pattern.subn(lambda m:m.group(1)+block+m.group(3),page,count=1)
        if n==0: raise RuntimeError(f'old related block missing for q{qid}')
    for q in raw:
        qid=q['id']; block=related_block(qid,all_items,rels[qid],html_stems,answers)
        page=page.replace(f'__RELATED_{qid}__',block)
    # Clicking a practice solution link opens that test's explanation.
    if 'id="history-back"' not in page:
        button='<button class="screen" id="history-back" type="button" disabled aria-label="بازگشت به جای قبلی" style="position:fixed;bottom:1rem;left:1rem;z-index:1000;border:0;border-radius:999px;padding:.65em 1.1em;background:#124f58;color:#fff;font:inherit;box-shadow:0 2px 8px #0002;cursor:pointer;opacity:.45">↶ بازگشت</button>'
        page=page.replace('</header>','</header>'+button,1)
    nav_script=(ROOT.parent/'history_navigation.js').read_text(encoding='utf-8').strip()
    if re.search(r'<script>.*?</script>(?=</body>)',page,re.S):
        page=re.sub(r'<script>.*?</script>(?=</body>)','<script>'+nav_script+'</script>',page,count=1,flags=re.S)
    else:
        page=page.replace('</body>', '<script>'+nav_script+'</script></body>')
    # Add the count to the HTML cover.
    if '۱۴۰ تست با حل تشریحی' not in page:
        page=page.replace('</header>','<p class="tag">۱۴۰ تست با پاسخ نهایی و حل تشریحی؛ ۷۰ تست بازنویسی‌شده با ارجاع منبع</p></header>',1)
    page=re.sub(r'(<bdi class="math" dir="ltr">)(.*?)(</bdi>)',lambda m:m.group(1)+style_math_html(m.group(2))+m.group(3),page)
    html_path.write_text(page)

    # Add new tests inside the matching TeX lemma and their full solutions in the answer section.
    question_end=tex.index('\\section*{پاسخ‌های تشریحی}')
    qpart=tex[:question_end]; spart=tex[question_end:]
    for qid,tip in OLD_SHORTCUTS.items():
        pat=re.compile(r'(\\paragraph\{تست\s+'+str(qid)+r'\}.*?)(?=\\paragraph\{تست|\\clearpage|\\section\*\{پاسخ)',re.S)
        m=pat.search(qpart)
        if m and 'نکتهٔ سریع' not in m.group(1):
            block=m.group(1).rstrip()+r'\par\textbf{نکتهٔ سریع.} '+math_tex(tip)
            qpart=qpart[:m.start(1)]+block+qpart[m.end(1):]
    # Add source-based tests before the next lemma/page break.
    for lesson,qs in new_by_lesson.items():
        if lesson<7:
            start=re.search(r'\\clearpage\\section\*\{لم\s+'+fa_digits(lesson)+r'(?=[\sـ])',qpart).start()
            nextm=re.search(r'\\clearpage\\section\*\{لم\s+'+fa_digits(lesson+1)+r'(?=[\sـ])',qpart[start+1:])
        else:
            start=re.search(r'\\clearpage\\section\*\{لم\s+۷(?=[\sـ])',qpart).start()
            nextm=None
        if nextm:
            end=start+1+nextm.start()
        else:
            end=len(qpart)
        snippets=[]
        for q in qs:
            source=q['source']+'، ص '+fa_digits(q['source_page'])
            options='　'.join(f'{fa_digits(i+1)}) {option_tex(v)}' for i,v in enumerate(q['choices']))
            snippets.append(f'\\paragraph{{تست {fa_digits(q["id"])}}} {source}\\par {math_tex(q["stem"])}\\par {options}\\par\\textbf{{نکتهٔ سریع.}} {math_tex(q["shortcut"])}\n')
        qpart=qpart[:end]+''.join(snippets)+qpart[end:]
    sol_snippets=[]
    for q in raw:
        sol_snippets.append(f'\\paragraph{{تست {fa_digits(q["id"])}؛ گزینهٔ {fa_digits(q["answer"])}}} {math_tex(q["solution"])}\\par\n')
    # Polish older terse solutions in TeX as well.
    for a,b in [('پیدا کن','به دست می‌آوریم'),('بگیر','در نظر می‌گیریم'),('بگذار','قرار می‌دهیم'),('بنویس','می‌نویسیم'),('کم کن','از دو طرف کم می‌کنیم'),('چک کن','بررسی می‌کنیم'),('فرض کن','فرض می‌کنیم'),('حساب کن','محاسبه می‌کنیم')]: spart=spart.replace(a,b)
    spart=re.sub(r'\\end\{document\}\s*$', '', spart)
    tex_path.write_text(math_style_tex(qpart+spart+''.join(sol_snippets)+'\\end{document}\n'))
    print(f'Built HTML and TeX with {len(raw)} new exam-adapted tests; total {len(all_items)}.')

if __name__=='__main__': main()
