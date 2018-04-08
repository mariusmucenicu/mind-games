import os
import sys
import web

from ast import literal_eval

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from mindgames import number_distance  # noqa

urls = (
    '/', 'Index',
    '/grade', 'Grade',
    '/play', 'Play',
    '/result', 'Result',
)

templates_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
templates_path = '{0}/templates'.format(templates_dir)
app = web.application(urls, globals())
render = web.template.render(templates_path, base='layout')


class Index:
    def GET(self):
        return render.index()


class Grade:
    def GET(self):
        return render.grade()


class Play:
    def POST(self):
        level = web.input().get('level')
        data = number_distance.play(level)
        return render.play(data)


class Result:
    def POST(self):
        data = literal_eval(web.input().get('raw_data'))
        answer = web.input().get('answer')
        result = number_distance.generate_results(data, answer)
        level = data.get('left_bound'), data.get('right_bound')
        question = '{0}{start}, {stop}{1}'.format(data.get('left_glyph'), data.get('right_glyph'),
                                                  start=data.get('start'), stop=data.get('stop'))

        if result[1]:
            return render.result_success(level)
        else:
            return render.result_failure(level, question, answer, result[0])


if __name__ == '__main__':
    if not ('WEBPY_ENV' in os.environ and os.environ['WEBPY_ENV'] == 'test'):
        app.run()
