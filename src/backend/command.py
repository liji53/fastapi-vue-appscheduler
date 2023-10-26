import click


@click.group()
@click.version_option(version="1.0.0")
def app_scheduler_command():
    pass


@app_scheduler_command.group("database")
def database_command():
    """数据库命令组"""
    pass


def init_database():
    from sqlalchemy_utils import create_database, database_exists
    from .core.config import DATABASE_URI
    from .core.database import engine, Base, SessionLocal
    from .auth.schemas import UserCreate
    from .auth import service as user_service
    from .permission.schemas import RoleCreate, MenuItem
    from .permission import service as permission_service
    from .application_category.schemas import ApplicationCategoryCreate
    from .application_category import service as app_category_service

    """初始化数据库"""
    if not database_exists(DATABASE_URI):
        create_database(DATABASE_URI)

    # 初始化表
    tables = [table for _, table in Base.metadata.tables.items()]
    Base.metadata.create_all(engine, tables=tables)

    db_session = SessionLocal()

    # 初始化菜单
    menus = permission_service.get_menus(db_session=db_session)
    if not menus:
        menus = []
        default_menus = [
            {
                "path": "/task",
                "meta": {"title": "任务中心", "icon": "listCheck", "rank": 2},
                "children": [
                    {
                        "path": "/task/index",
                        "name": "Task",
                        "meta": {"title": "任务中心"}
                    }
                ]
            },
            {
                "path": "/app",
                "meta": {"title": "应用中心", "icon": "menu", "rank": 4},
                "children": [
                    {
                        "path": "/app/manager",
                        "name": "App",
                        "meta": {"title": "应用管理"}
                    },
                    {
                        "path": "/app/store",
                        "name": "Store",
                        "meta": {"title": "应用商城"}
                    }
                ]
            },
            {
                "path": "/monitor",
                "meta": {"title": "监控中心", "icon": "monitor", "rank": 8},
                "children": [
                    {
                        "path": "/monitor/exception",
                        "name": "Exception",
                        "meta": {"title": "异常监控"}
                    },
                    {
                        "path": "/monitor/statistics",
                        "name": "Statistics",
                        "meta": {"title": "统计管理"}
                    },
                    {
                        "path": "/monitor/resource",
                        "name": "Resource",
                        "meta": {"title": "系统资源"}
                    }
                ]
            },
            {
                "path": "/security",
                "meta": {"title": "安全中心", "icon": "flUser", "rank": 10},
                "children": [
                    {
                        "path": "/security/user/index",
                        "name": "User",
                        "meta": {"title": "用户管理"}
                    },
                    {
                        "path": "/security/config",
                        "name": "Config",
                        "meta": {"title": "系统配置"}
                    }
                ]
            }
        ]
        for default_menu in default_menus:
            menus += permission_service.create_menus(
                db_session=db_session,
                menu_in=MenuItem(**default_menu)
            )

    # 初始化admin角色
    role = permission_service.get_role_by_code(code="admin", db_session=db_session)
    if not role:
        role = permission_service.create_role(db_session=db_session,
                                              role_in=RoleCreate(name="管理员", code="admin", menus=menus))

    # 初始化admin用户
    user = user_service.get_by_name(username="admin", db_session=db_session)
    if not user:
        user_service.create(user_in=UserCreate(username="admin", password="admin123", roles=[role]),
                            db_session=db_session)

    # 初始化app category
    app_categories = app_category_service.get_all(db_session=db_session)
    if not app_categories:
        app_category_service.create(db_session=db_session, app_category_in=ApplicationCategoryCreate(name="规范递交"))
        app_category_service.create(db_session=db_session, app_category_in=ApplicationCategoryCreate(name="数据比对"))


def get_alembic_config():
    from alembic.config import Config
    from .core.config import DATABASE_URI, ALEMBIC_INI_PATH

    alembic_cfg = Config(ALEMBIC_INI_PATH)
    alembic_cfg.set_main_option("sqlalchemy.url", str(DATABASE_URI))
    return alembic_cfg


@database_command.command("add")
def database_add():
    """用于测试"""
    from .core.database import SessionLocal
    from .application.schemas import ApplicationCreate
    from .application_category.schemas import ApplicationCategoryCreate
    from .application import service as app_service

    db_session = SessionLocal()
    test_apps = [
        {"name": "test1", "description": "111", "banner": "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
         "category": ApplicationCategoryCreate(name="规范递交"), "status": "已发布"},
        {"name": "test2", "description": "222", "banner": "https://tdesign.gtimg.com/tdesign-pro/t-sec.jpg",
         "category": ApplicationCategoryCreate(name="规范递交"), "status": "已发布"},
        {"name": "test3", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
         "category": ApplicationCategoryCreate(name="数据比对"), "status": "已发布"},
        {"name": "test4", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "废弃"},
        {"name": "test5", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/t-sec.jpg",
         "category": ApplicationCategoryCreate(name="数据比对"), "status": "废弃"},
        {"name": "test6", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "废弃"},
        {"name": "test7", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "废弃"},
        {"name": "test8", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "废弃"},
        {"name": "test9", "description": None, "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg",
         "category": ApplicationCategoryCreate(name="数据比对"), "status": "废弃"},
        {"name": "test10", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "已发布"},
        {"name": "test11", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "已发布"},
        {"name": "test12", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "已发布"},
        {"name": "test13", "description": "", "banner": None, "status": "废弃"},
        {"name": "test14", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "废弃"},
        {"name": "test55", "description": "333", "status": "废弃"},
        {"name": "test66", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "已发布"},
        {"name": "test77", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "废弃"},
        {"name": "test88", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "已发布"},
        {"name": "test99", "description": "333", "banner": "https://tdesign.gtimg.com/tdesign-pro/ssl.jpg", "status": "废弃"},
    ]
    for app in test_apps:
        app_service.create(db_session=db_session, application_in=ApplicationCreate(**app))
    click.secho("Success.", fg="green")


@database_command.command("init")
def database_init():
    from alembic import command as alembic_command

    click.echo("Initializing new database...")
    init_database()
    # 指定为初始版本
    alembic_command.stamp(get_alembic_config(), "head")
    click.secho("Success.", fg="green")


@database_command.command("drop")
@click.option("--yes", is_flag=True, help="Silences all confirmation prompts.")
def drop_database(yes):
    from sqlalchemy_utils import drop_database, database_exists
    from .core.config import DATABASE_URI, DATABASE_HOSTNAME, DATABASE_NAME

    if database_exists(str(DATABASE_URI)):
        if yes:
            drop_database(str(DATABASE_URI))
            click.secho("Success.", fg="green")

        if click.confirm(f"Are you sure to drop: '{DATABASE_HOSTNAME}:{DATABASE_NAME}'?"):
            drop_database(str(DATABASE_URI))
            click.secho("Success.", fg="green")
    else:
        click.secho(
            f"'{DATABASE_HOSTNAME}:{DATABASE_NAME}' does not exist!!!", fg="red"
        )


@database_command.command("revision")
@click.option("-m", "--message", default=None, help="Revision message")
def revision_database(message):
    """生成迁移脚本"""
    from alembic import command as alembic_command

    alembic_command.revision(
        get_alembic_config(),
        message,
        autogenerate=True  # 无法检测：1.表名、列名的变化 2.匿名的约束
    )


@database_command.command("upgrade")
@click.option("--revision", nargs=1, default="head", help="Revision identifier.")
def upgrade_database(revision):
    from sqlalchemy_utils import database_exists
    from alembic import command as alembic_command

    from .core.config import DATABASE_URI

    if not database_exists(str(DATABASE_URI)):
        click.secho("Database not exist, initializing new database...")
        init_database()
        # 指定为初始版本
        alembic_command.stamp(get_alembic_config(), "head")
    else:
        alembic_command.upgrade(get_alembic_config(), revision)

    click.secho("Success.", fg="green")


@database_command.command("history")
def history_database():
    from alembic import command as alembic_command

    alembic_command.history(get_alembic_config())


@database_command.command("downgrade")
@click.option("--revision", nargs=1, default="head", help="Revision identifier.")
def downgrade_database(revision):
    from alembic import command as alembic_command

    alembic_command.downgrade(get_alembic_config(), revision)
    click.secho("Success.", fg="green")


def entrypoint():
    # try:
    #     app_scheduler_command()
    # except Exception as e:
    #     click.secho(f"ERROR: {e}", bold=True, fg="red")
    app_scheduler_command()


if __name__ == "__main__":
    entrypoint()
