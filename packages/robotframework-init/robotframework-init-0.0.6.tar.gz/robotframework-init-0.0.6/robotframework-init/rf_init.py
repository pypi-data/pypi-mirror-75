#!/usr/local/opt/python/bin/python3.7
import os
import shutil
import click


@click.command()
@click.option('--project_name', prompt='请输入项目名称', help='项目名称')
@click.option('--target_dir', default='.', help='项目存放路径')
def rf_init(project_name, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        click.echo(f'目标路径 {target_dir} 不存在，现已创建成功！')
    project_dir = os.path.join(target_dir, project_name)
    if os.path.exists(project_dir):
        click.echo(f'项目名称 {project_name} 在目标路径 {target_dir} 已存在，无需重复初始化！')
    else:
        os.mkdir(project_dir)
        keyword = os.path.join(project_dir, 'keyword')
        pages = os.path.join(project_dir, 'pages')
        testcases = os.path.join(project_dir, 'testcases')
        reports = os.path.join(project_dir, 'reports')
        lib = os.path.join(project_dir, 'lib')
        children_dir = [keyword, pages, testcases, reports, lib]
        [os.mkdir(dir) for dir in children_dir]
        resource_dir = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), 'resource')
        for f in os.listdir(resource_dir):
            src_path = os.path.join(resource_dir, f)
            dst_path = os.path.join(project_dir, f)
            shutil.copyfile(src_path, dst_path)
        click.echo(f'项目名称 {project_name} 在目标路径 {target_dir} 初始化成功！')


if __name__ == '__main__':
    rf_init()
