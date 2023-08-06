"""Order Management Module base on vtex docs on
https://documenter.getpostman.com/view/487146/S1LyUnDN?version=latest
"""
from collections import namedtuple
from datetime import datetime

from .base_api import BaseApi

Res = namedtuple("result", ["json", "total_pages", "status_code"])


class OrderManagementApi(BaseApi):
    """
    Order Management get functions for different endpoints
    """

    def _build_url(self, endpoint):
        url = self.base_url + f"/api/oms/pvt/orders"
        return url + endpoint

    def get_order(self, order_id):
        """
        Given an order_id, return the information into a json dict
        :param order_id: str
        :return: json dictionary
        """
        endpoint = f"/{order_id}"
        url = self._build_url(endpoint)
        return self.get_result(url)

    def get_list_orders(
            self, initial_date: datetime = datetime(2000, 1, 1), page: int = 1
    ):
        """
        Given an initial datetime objects and page (by default returns the first page),
        returns a json dict, containing a list with orders
        :param initial_date: datetime
        :param page: int
        :return: json dictionary
        """
        end_dt = datetime.today()
        url = self._build_url(
            f"?f_creationDate=creationDate:["
            f"{initial_date.date()}T00:00:00.000Z TO "
            f"{end_dt.date()}T23:59:59.999Z]"
        )
        params = {"page": f"{page}", "orderBy": "creationDate,asc"}
        result = self.session.get(url, params=params, timeout=self.timeout)
        if result.status_code == 200:
            json_response = result.json()
            total_pages = json_response["paging"]["pages"]
            return Res(json_response, total_pages, result.status_code)
        return Res(None, None, result.status_code)

    def get_list_orders_by_page(self, page: int = 1):
        """
        Given a page, return the orders list from that page
        :param page:
        :return: json dictionary
        """
        url = self._build_url(
            f"?page={page}"
        )
        result = self.session.get(url, timeout=self.timeout)
        if result.status_code == 200:
            json_response = result.json()
            total_pages = json_response["paging"]["pages"]
            return Res(json_response, total_pages, result.status_code)
        return Res(None, None, result.status_code)

    def get_conversation(self, order_id):
        """
        Given an order_id, returns its conversation history
        :param order_id: str
        :return: json dict
        """
        url = self._build_url(f"/{order_id}/conversation-message")
        return self.get_result(url)

    def get_payment_transaction(self, order_id):
        """
        Given an order_id, returns the transaction information
        :param order_id:
        :return: json-dict
        """
        url = self._build_url(f"/{order_id}/payment-transaction")
        return self.get_result(url)
