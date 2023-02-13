import os

import aiosqlite

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"


async def get_blacklisted_users() -> list:
    """
    This function will return the list of all blacklisted users.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT user_id, strftime('%s', created_at) FROM blacklist"
        ) as cursor:
            result = await cursor.fetchall()
            return result


async def is_blacklisted(user_id: int) -> bool:
    """
    This function will check if a user is blacklisted.

    :param user_id: The ID of the user that should be checked.
    :return: True if the user is blacklisted, False if not.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT * FROM blacklist WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def add_user_to_blacklist(user_id: int) -> int:
    """
    This function will add a user based on its ID in the blacklist.

    :param user_id: The ID of the user that should be added into the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This function will remove a user based on its ID from the blacklist.

    :param user_id: The ID of the user that should be removed from the blacklist.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def add_warn(user_id: int, server_id: int, moderator_id: int, reason: str) -> int:
    """
    This function will add a warn to the database.

    :param user_id: The ID of the user that should be warned.
    :param reason: The reason why the user should be warned.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await db.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await db.commit()
            return warn_id


async def remove_warn(warn_id: int, user_id: int, server_id: int) -> int:
    """
    This function will remove a warn from the database.

    :param warn_id: The ID of the warn.
    :param user_id: The ID of the user that was warned.
    :param server_id: The ID of the server where the user has been warned
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await db.commit()
        rows = await db.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_warnings(user_id: int, server_id: int) -> list:
    """
    This function will get all the warnings of a user.

    :param user_id: The ID of the user that should be checked.
    :param server_id: The ID of the server that should be checked.
    :return: A list of all the warnings of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list


async def get_user_todos(user_id: int) -> list:
    """
    This function will return the list of all todos of a user.

    :param user_id: The ID of the user that should be checked.
    :return: A list of the todos of the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            f"SELECT task FROM todos WHERE user_id = {user_id}"
        ) as cursor:
            result = await cursor.fetchall()
            return result


async def clear_user_todos(user_id: int):
    """
    This function will clear the list of all todos of a user.

    :param user_id: The ID of the user that should be checked.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM todos WHERE user_id=?", (user_id,))
        await db.commit()


async def add_todo(user_id: int, todo: str):
    """
    This function will add a user's todo to the database.

    :param user_id: The ID of the user whose todo is to be added.
    :param todo: The task to be assigned to the user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO todos(user_id, task) VALUES (?, ?)",
            (user_id, todo),
        )
        await db.commit()
        return todo


async def delete_user_todo(user_id: int, task_id: int):
    """
    This function will delete a particular task of a user.

    :param user_id: The ID of the user that should be checked.
    :param task_id: The task number of the todo to delete
    """
    task_result = ""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            f"SELECT task FROM todos WHERE user_id = {user_id}"
        ) as cursor:
            result = await cursor.fetchall()
            for each in enumerate(result, 1):
                if each[0] == task_id:
                    task_result = each[1][0]
                    print(task_result)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f"DELETE FROM todos WHERE task='{task_result}';")
        await db.commit()
        return task_result


async def add_rep(user_id: int, rep_count: int):
    """
    This function will add reputation to a user in the database.

    :param user_id: The ID of the user whose todo is to be added.
    :param rep_count: The number of reps to be added to a user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            f"SELECT * from reputation where user_id = {user_id}"
        ) as cursor:
            result = await cursor.fetchall()
            if result:
                await db.execute(
                    "UPDATE reputation SET rep = rep + ? WHERE user_id = ?;",
                    (rep_count, user_id),
                )
                await db.commit()
            else:
                await db.execute(
                    "INSERT INTO reputation(user_id, rep) VALUES (?, ?)",
                    (user_id, rep_count),
                )
                await db.commit()


async def get_user_rep(user_id: int) -> list:
    """
    This function will return the reputation count of a user.

    :param user_id: The ID of the user that should be checked.
    :return: The reputation count of the requested user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(f"SELECT * FROM reputation ORDER BY rep DESC") as cursor:
            result = await cursor.fetchall()
            if result:
                for each in enumerate(result, 1):
                    if each[1][0] == str(user_id):
                        return each
            return None


async def del_rep(user_id: int, rep_count: int):
    """
    This function will delete reputation from a user in the database.

    :param user_id: The ID of the user whose todo is to be added.
    :param rep_count: The number of reps to be deleted from a user.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            f"SELECT * from reputation where user_id = {user_id}"
        ) as cursor:
            result = await cursor.fetchall()
            if result:
                await db.execute(
                    "UPDATE reputation SET rep = rep - ? WHERE user_id = ?;",
                    (rep_count, user_id),
                )
                await db.commit()


async def clear_rep():
    """
    This function will delete all reputation from all users in the database.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM reputation;")
        await db.commit()


async def get_all_rep() -> list:
    """
    This function will return the all reputation points of all users.

    :return: The reputation list.
    """
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(f"SELECT * FROM reputation ORDER BY rep DESC") as cursor:
            result = await cursor.fetchall()
            rep_data = []
            for each in enumerate(result, 1):
                res = []
                for x in each[0], each[1][0], each[1][1]:
                    res.append(x)
                rep_data.append(res)
            return rep_data
