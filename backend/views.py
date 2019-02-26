import base64
from django.shortcuts import render
from django.http import HttpResponse
from latex import build_pdf, LatexBuildError
from django.shortcuts import render

# Create your views here.


def test_view_latex(request):
    if request.method == 'POST':
        print(request.POST)
    latex = (open("test.latex"))
    b64_data = ""
    try:
        pdf = build_pdf(latex)
        pdf.save_to('test.pdf')
        b64_data = base64.b64encode(pdf.data)
    except LatexBuildError as e:
        for err in e.get_errors():
            print(u'Error in {0[filename]}, line {0[line]}: {0[error]}'.format(err))
            # also print one line of context
            print(u'    {}'.format(err['context'][1]))
            context = ""
    # convert to base64
    context = {
        'data': b64_data
    }
    return render(request, 'index.html', context)
