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
    from .auth.schemas import UserRegister
    from .auth.service import get_user_by_name, create_user
    from .permission.schemas import RoleRegister
    from .permission.service import get_role_by_name, create_role

    """初始化数据库"""
    if not database_exists(DATABASE_URI):
        create_database(DATABASE_URI)

    # 初始化表
    tables = [table for _, table in Base.metadata.tables.items()]
    Base.metadata.create_all(engine, tables=tables)

    # 初始化admin角色、用户
    db_session = SessionLocal()
    role = get_role_by_name(name="admin", db_session=db_session)
    if not role:
        role = create_role(db_session=db_session, role_in=RoleRegister(name="admin"))

    user = get_user_by_name(username="admin", db_session=db_session)
    if not user:
        create_user(user_in=UserRegister(username="admin", password="admin123", roles=[role]), db_session=db_session)


def get_alembic_config():
    from alembic.config import Config
    from .core.config import DATABASE_URI, ALEMBIC_INI_PATH

    alembic_cfg = Config(ALEMBIC_INI_PATH)
    alembic_cfg.set_main_option("sqlalchemy.url", str(DATABASE_URI))
    return alembic_cfg


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
    try:
        app_scheduler_command()
    except Exception as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
