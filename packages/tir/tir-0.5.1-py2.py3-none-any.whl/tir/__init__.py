import logging
import os
import shutil

import pkg_resources
import sass
from jinja2 import Environment, FileSystemLoader

from tir.posts import Post
from tir.settings import REQUIRED_PATHS
from tir.tools import is_init, _, minify_file
from tir.utils import mktree, url_for, format_date

logger = logging.getLogger(__name__)


def init():
    if is_init():
        return False
    print('Initializing Tir project...')
    skeleton_dirs = REQUIRED_PATHS
    skeleton_files = ['tir.yml']
    for skeleton_dir in skeleton_dirs:
        mktree(skeleton_dir)
    for skeleton_file in skeleton_files:
        shutil.copyfile(pkg_resources.resource_filename('tir', 'data/{}'.format(skeleton_file)),
                        '{}/{}'.format(os.getcwd(), skeleton_file))
    shutil.copytree(pkg_resources.resource_filename('tir', 'visuals'),
                    '{}/{}'.format(os.getcwd(), 'visuals'))
    print('Tir project was successfully installed.')
    return True


class Tir(object):

    def __init__(self, conf):
        """Tir def

        Performs some checks on the environment before doing anything else.
        """

        self.conf = conf

        self.theme = self.conf.get('visuals').get('theme') or 'default'
        self.build_dir = self.conf['build_dir']

    def build(self):
        if not is_init():
            print('Project does not seem to be initialized. Type "tir init" to create a Tir project here.')
            return False
        try:
            pkg_data_dir = pkg_resources.resource_filename('tir', 'data')
            tpl_visuals_dir = os.path.join(pkg_data_dir, 'visuals', self.theme)
            print('Selected template: %s', tpl_visuals_dir)
            print('Replace assets files')
            assets_src_dir = os.path.join(tpl_visuals_dir, 'assets')
            assets_target_dir = os.path.join(os.getcwd(), self.build_dir, 'static')
            print('Removing {}'.format(assets_target_dir))
            if os.path.exists(assets_target_dir):
                shutil.rmtree(assets_target_dir)
            shutil.copytree(assets_src_dir, assets_target_dir)
            print('Assets successfully updated')
            env = Environment(
                loader=FileSystemLoader(os.path.join(tpl_visuals_dir, 'templates')),
                autoescape=True
            )
            post_tpl = env.get_template('post.html')
            index_tpl = env.get_template('home.html')
            env.globals['url_for'] = url_for
            env.globals['_'] = _
            env.globals['format_date'] = format_date
            env.globals['config'] = self.conf

            print('Building static files...')
            scss_dir = os.path.join(assets_target_dir, 'scss')
            css_dir = os.path.join(assets_target_dir, 'css')
            print('Scanning {}'.format(os.path.join(scss_dir)))
            mktree(css_dir)
            compiled_scss = sass.compile(filename=os.path.join(scss_dir, 'main.scss'))
            stylesheet_path = os.path.join(css_dir, 'stylesheet.css')
            with open(stylesheet_path, 'w+') as f:
                f.write(compiled_scss)
            minified_stylesheet_path = minify_file(stylesheet_path)

            print('Building content...')
            slugs = Post.get_slugs()
            for slug in slugs:
                slug = slug.replace('.md', '')
                p = Post()
                x = p.read(slug)
                target_path = '%s/%s.html' % (self.build_dir, slug)
                mktree(self.build_dir)
                with open(target_path, 'w', encoding='utf-8') as fh:
                    head = {'title': x.meta['title'],
                            'description': x.meta['subtitle'], 'stylesheet_file_name': minified_stylesheet_path}
                    fh.write(post_tpl.render(
                        post=p,
                        head=head,
                    ))
                print('Compiling {}...'.format(target_path))

            # Building index page
            print('Building index page...')
            with open(self.build_dir + '/index.html', 'w', encoding='utf-8') as fh:
                p = Post()
                x = p.read('index', dir_path=Post.MISC_DIR)
                head = {'title': 'ouafi.net', 'description': 'Dans un monde fou, toute forme d\'écriture est un '
                                                             'remède psychiatrique',
                        'stylesheet_file_name': minified_stylesheet_path}
                fh.write(index_tpl.render(
                    content={'intro': x},
                    post=p,
                    head=head
                ))

            print('Build was successful.')
            return True

        except Exception as e:
            raise e
