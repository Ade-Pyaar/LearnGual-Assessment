from random import choices
import string


from django.core.paginator import Paginator


from rest_framework.response import Response


def snake_case_to_camel_case(value: str):
    splitted_string = value.split("_")

    camel_string = splitted_string.pop(0)

    for other_words in splitted_string:
        camel_string += other_words.title()

    return camel_string


class APIResponses:
    @classmethod
    def success_response(cls, message: str, status_code, data=None, paginate_data=None):
        context = {
            "success": True,
            "message": message,
        }

        if data is not None:
            context["data"] = data

            if paginate_data:
                context["pagination"] = paginate_data

        return Response(context, status=status_code)

    @classmethod
    def error_response(cls, status_code, message, errors: dict = None):
        context = {
            "success": False,
            "message": message,
        }

        if errors is not None:
            errors_list = []
            for key, value in errors.items():
                if isinstance(value, list):
                    value = value[0]

                key = snake_case_to_camel_case(key)

                errors_list.append({"fieldName": key, "error": value})

            context["errors"] = errors_list

            errors_message_list = [value[0] for value in errors.values()]
            message = errors_message_list[0]

            context["message"] = message

        return Response(context, status=status_code)

    @classmethod
    def server_error(cls, message: str, status_code):
        context = {"success": False, "message": message}

        return Response(context, status=status_code)


class CodeGenerator:
    @staticmethod
    def generate_ws_token():
        code_list = choices(string.digits + string.ascii_uppercase, k=15)

        code = "".join(code_list)
        return code


class MyPagination:
    @classmethod
    def get_paginated_response(cls, request, queryset):
        page_number = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 25)

        paginator = Paginator(queryset, page_size)
        try:
            current_page = paginator.page(page_number)
        except Exception:
            return None, None, "Invalid page number"

        total_data = {
            "currentPage": current_page.number,
            "numberOfPages": paginator.num_pages,
            "nextPage": current_page.next_page_number()
            if current_page.has_next()
            else None,
            "previousPage": current_page.previous_page_number()
            if current_page.has_previous()
            else None,
        }

        return total_data, current_page.object_list, None
