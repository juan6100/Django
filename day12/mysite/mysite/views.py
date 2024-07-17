#처리된 데이터를 갖고 어떠한 기능을 하는게 뷰이다
from django.shortcuts import render,get_object_or_404


#리스트의 화면
def post_list(request):
    return render(request,'blog/main.html')
#게시물 상세 뷰
