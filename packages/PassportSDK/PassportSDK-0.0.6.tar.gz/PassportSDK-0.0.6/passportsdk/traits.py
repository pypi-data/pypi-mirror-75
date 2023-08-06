
class AuthTrait:
    @staticmethod
    def get_access_token(app_client):
        """
        获取access_token
        :return:
        """
        from passportsdk.common import post

        if not app_client.access_token:
            json_data = {
                'access_key_id': app_client.access_key_id,
                'access_key_secret': app_client.access_key_secret
            }
            res = post(
                url='%s/user/access/token' % app_client.passport_service_url,
                json_data=json_data,
                headers=None
            )
            if res and 'data' in res and 'access_token' in res['data']:
                # print('[[get_access_token: ', res['data']['access_token'])
                app_client.access_token = res['data']['access_token']
                return app_client.access_token
            return None
        return app_client.access_token

    @staticmethod
    def user_register(app_client, username, password):
        """
        用户注册
        :param username:
        :param password:
        :return:
        """
        json_data = {
            'username': username,
            'password': password
        }
        res = app_client.post(
            url='/user/register',
            json_data=json_data
        )
        return res

    @staticmethod
    def user_login(app_client, username, password):
        """
        用户登录
        :param username:
        :param password:
        :return:
        """
        json_data = {
            'username': username,
            'password': password
        }
        res = app_client.post(
            url='/user/login',
            json_data=json_data
        )
        print(res)
        return res

    @staticmethod
    def user_logout(app_client, user_token):
        """
        用户登出
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/user/logout',
            json_data=json_data
        )
        return res

    @staticmethod
    def user_info(app_client, user_token):
        """
        用户信息
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/user/info',
            json_data=json_data
        )
        return res


class AdminTrait:

    @staticmethod
    def admin_user_list(app_client, user_token, request_data):
        """
        [后台]用户列表
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
            'current_page': request_data.get('current_page', 1),
            'per_page': request_data.get('per_page', 10),
        }
        res = app_client.post(
            url='/admin/user/list',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_user_info(app_client, user_token, user_uuid):
        """
        [后台]用户信息
        :param user_token:
        :param user_id:
        :return:
        """
        json_data = {
            'token': user_token,
            'user_uuid': user_uuid
        }
        res = app_client.post(
            url='/admin/user/info',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_user_modify(app_client, user_token, user_uuid, modify_user_info):
        """
        [后台]用户编辑(创建)
        :param user_token:
        :param user_id:
        :param modify_user_info:
        :return:
        """
        json_data = {
            'token': user_token,
            'user_uuid': user_uuid,
            'username': modify_user_info['username'],
            'password': modify_user_info['password'],
            'permissions': modify_user_info['permissions'],
            'roles': modify_user_info['roles'],
            'groups': modify_user_info['groups']
        }
        res = app_client.post(
            url='/admin/user/modify',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_user_delete(app_client, user_token, user_uuid):
        """
        [后台]用户删除
        :param user_token:
        :param user_id:
        :return:
        """
        json_data = {
            'token': user_token,
            'user_uuid': user_uuid,
        }
        res = app_client.post(
            url='/admin/user/delete',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_permission_list(app_client, user_token):
        """
        [后台]权限列表
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/admin/permission/list',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_permission_info(app_client, user_token, permission_id):
        """
        [后台]权限信息
        :param user_token:
        :param permission_id:
        :return:
        """
        json_data = {
            'token': user_token,
            'permission_id': permission_id
        }
        res = app_client.post(
            url='/admin/permission/info',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_permission_modify(app_client, user_token, permission_id, modify_permission_info):
        """
        [后台]权限编辑(创建)
        :param user_token:
        :param user_id:
        :param modify_user_info:
        :return:
        """
        json_data = {
            'token': user_token,
            'permission_id': permission_id,
            'modify_permission_info': modify_permission_info
        }
        res = app_client.post(
            url='/admin/permission/modify',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_role_list(app_client, user_token):
        """
        [后台]角色列表
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/admin/role/list',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_role_info(app_client, user_token, role_id):
        """
        [后台]角色信息
        :param user_token:
        :param role_id:
        :return:
        """
        json_data = {
            'token': user_token,
            'role_id': role_id
        }
        res = app_client.post(
            url='/admin/role/info',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_role_modify(app_client, user_token, role_id, modify_role_info):
        """
        [后台]角色编辑(创建)
        :param user_token:
        :param role_id:
        :param modify_role_info:
        :return:
        """
        json_data = {
            'token': user_token,
            'role_id': role_id,
            'modify_role_info': modify_role_info
        }
        res = app_client.post(
            url='/admin/role/modify',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_group_list(app_client, user_token):
        """
        [后台]用户组列表
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/admin/group/list',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_group_info(app_client, user_token, group_id):
        """
        [后台]用户组信息
        :param user_token:
        :param group_id:
        :return:
        """
        json_data = {
            'token': user_token,
            'group_id': group_id
        }
        res = app_client.post(
            url='/admin/group/info',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_group_modify(app_client, user_token, group_id, modify_group_info):
        """
        [后台]用户组编辑(创建)
        :param user_token:
        :param group_id:
        :param modify_group_info:
        :return:
        """
        json_data = {
            'token': user_token,
            'group_id': group_id,
            'modify_group_info': modify_group_info
        }
        res = app_client.post(
            url='/admin/group/modify',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_app_list(app_client, user_token):
        """
        [后台]应用组列表
        :param user_token:
        :return:
        """
        json_data = {
            'token': user_token,
        }
        res = app_client.post(
            url='/admin/app/list',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_app_info(app_client, user_token, app_id):
        """
        [后台]应用组信息
        :param user_token:
        :param app_id:
        :return:
        """
        json_data = {
            'token': user_token,
            'app_id': app_id
        }
        res = app_client.post(
            url='/admin/app/info',
            json_data=json_data
        )
        return res

    @staticmethod
    def admin_app_modify(app_client, user_token, app_id, modify_app_info):
        """
        [后台]应用组编辑(创建)
        :param user_token:
        :param app_id:
        :param modify_app_info:
        :return:
        """
        json_data = {
            'token': user_token,
            'app_id': app_id,
            'modify_app_info': modify_app_info
        }
        res = app_client.post(
            url='/admin/app/modify',
            json_data=json_data
        )
        return res
