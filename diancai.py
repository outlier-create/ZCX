import os
import sys
from datetime import datetime

class RestaurantOrderingSystem:
    def __init__(self):
        self.menu = {
            "鱼香肉丝": 28.0,
            "宫保鸡丁": 32.0,
            "麻婆豆腐": 18.0,
            "糖醋排骨": 42.0,
            "红烧肉": 45.0,
            "清蒸鱼": 68.0,
            "炒时蔬": 22.0,
            "紫菜蛋花汤": 16.0,
            "番茄鸡蛋汤": 16.0,
            "米饭": 2.0
        }
        self.order = {}
        self.discount_rate = 1.0
        self.receipt_number = self._generate_receipt_number()

    def _generate_receipt_number(self):
        """生成唯一的订单号"""
        now = datetime.now()
        return f"R{now.strftime('%Y%m%d%H%M%S')}"

    def display_menu(self):
        """显示菜单"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 50)
        print(f"{'菜单'.center(48)}")
        print("=" * 50)
        print("序号\t菜名\t\t价格(元)")
        print("-" * 50)
        for idx, (dish, price) in enumerate(self.menu.items(), 1):
            print(f"{idx:<8}{dish:<16}{price}")
        print("=" * 50)

    def add_to_order(self):
        """添加菜品到订单"""
        while True:
            self.display_menu()
            print("\n请输入要添加的菜品编号或名称（输入'q'返回主菜单）：")
            choice = input("> ").strip()

            if choice.lower() == 'q':
                break

            # 处理菜品编号
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(self.menu):
                    dish = list(self.menu.keys())[idx - 1]
                else:
                    print("无效的菜品编号，请重新输入！")
                    input("按Enter继续...")
                    continue
            # 处理菜品名称
            else:
                dish = choice
                if dish not in self.menu:
                    print("菜单中没有此菜品，请重新输入！")
                    input("按Enter继续...")
                    continue

            # 输入数量
            while True:
                try:
                    quantity = int(input(f"请输入'{dish}'的数量：").strip())
                    if quantity <= 0:
                        print("数量必须大于0，请重新输入！")
                    else:
                        break
                except ValueError:
                    print("请输入有效的数字！")

            # 添加到订单
            if dish in self.order:
                self.order[dish] += quantity
            else:
                self.order[dish] = quantity

            print(f"已添加 {quantity}份 '{dish}' 到订单！")
            input("按Enter继续...")

    def remove_from_order(self):
        """从订单中移除菜品"""
        if not self.order:
            print("订单为空！")
            input("按Enter继续...")
            return

        while True:
            self.display_order()
            print("\n请输入要移除的菜品编号或名称（输入'q'返回主菜单）：")
            choice = input("> ").strip()

            if choice.lower() == 'q':
                break

            # 处理菜品编号
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(self.order):
                    dish = list(self.order.keys())[idx - 1]
                else:
                    print("无效的菜品编号，请重新输入！")
                    input("按Enter继续...")
                    continue
            # 处理菜品名称
            else:
                dish = choice
                if dish not in self.order:
                    print("订单中没有此菜品，请重新输入！")
                    input("按Enter继续...")
                    continue

            # 输入要移除的数量
            while True:
                try:
                    print(f"当前'{dish}'的数量：{self.order[dish]}")
                    quantity = int(input(f"请输入要移除的数量（输入0移除全部）：").strip())
                    if quantity < 0 or quantity > self.order[dish]:
                        print(f"数量无效，范围应为0-{self.order[dish]}，请重新输入！")
                    else:
                        break
                except ValueError:
                    print("请输入有效的数字！")

            # 从订单中移除
            if quantity == 0 or quantity == self.order[dish]:
                del self.order[dish]
                print(f"已从订单中移除 '{dish}'！")
            else:
                self.order[dish] -= quantity
                print(f"已从订单中移除 {quantity}份 '{dish}'！")

            input("按Enter继续...")

    def display_order(self):
        """显示当前订单"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 50)
        print(f"{'当前订单'.center(48)}")
        print(f"订单号: {self.receipt_number}")
        print("=" * 50)
        print("序号\t菜名\t\t单价(元)\t数量\t小计(元)")
        print("-" * 50)

        if not self.order:
            print("订单为空")
        else:
            total = 0
            for idx, (dish, quantity) in enumerate(self.order.items(), 1):
                price = self.menu[dish]
                subtotal = price * quantity
                total += subtotal
                print(f"{idx:<8}{dish:<16}{price:<12}{quantity:<8}{subtotal}")

            print("-" * 50)
            print(f"总计: {total}元")
            if self.discount_rate != 1.0:
                discounted_total = total * self.discount_rate
                print(f"折扣: {self.discount_rate * 10}折")
                print(f"实付: {discounted_total:.2f}元")
        print("=" * 50)

    def set_discount(self):
        """设置折扣率"""
        while True:
            try:
                discount = float(input("请输入折扣率（例如：0.8表示8折，1.0表示无折扣）：").strip())
                if 0 < discount <= 1.0:
                    self.discount_rate = discount
                    print(f"已设置折扣率为 {discount * 10}折！")
                    break
                else:
                    print("折扣率必须在0-1之间，请重新输入！")
            except ValueError:
                print("请输入有效的数字！")
        input("按Enter继续...")

    def generate_receipt(self):
        """生成并显示收据"""
        if not self.order:
            print("订单为空，无法生成收据！")
            input("按Enter继续...")
            return

        self.display_order()
        print("\n" + "=" * 50)
        print(f"{'收据'.center(48)}")
        print("=" * 50)
        print(f"订单号: {self.receipt_number}")
        print(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        print("菜名\t\t单价(元)\t数量\t小计(元)")
        print("-" * 50)

        total = 0
        for dish, quantity in self.order.items():
            price = self.menu[dish]
            subtotal = price * quantity
            total += subtotal
            print(f"{dish:<16}{price:<12}{quantity:<8}{subtotal}")

        print("-" * 50)
        print(f"总计: {total}元")
        if self.discount_rate != 1.0:
            discounted_total = total * self.discount_rate
            print(f"折扣: {self.discount_rate * 10}折")
            print(f"实付: {discounted_total:.2f}元")
        print("=" * 50)
        print("\n感谢惠顾，欢迎下次再来！")
        input("按Enter返回主菜单...")

    def save_receipt_to_file(self):
        """将收据保存到文件"""
        if not self.order:
            print("订单为空，无法保存收据！")
            input("按Enter继续...")
            return

        filename = f"receipt_{self.receipt_number}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write(f"{'收据'.center(48)}\n")
                f.write("=" * 50 + "\n")
                f.write(f"订单号: {self.receipt_number}\n")
                f.write(f"日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
                f.write("菜名\t\t单价(元)\t数量\t小计(元)\n")
                f.write("-" * 50 + "\n")

                total = 0
                for dish, quantity in self.order.items():
                    price = self.menu[dish]
                    subtotal = price * quantity
                    total += subtotal
                    f.write(f"{dish:<16}{price:<12}{quantity:<8}{subtotal}\n")

                f.write("-" * 50 + "\n")
                f.write(f"总计: {total}元\n")
                if self.discount_rate != 1.0:
                    discounted_total = total * self.discount_rate
                    f.write(f"折扣: {self.discount_rate * 10}折\n")
                    f.write(f"实付: {discounted_total:.2f}元\n")
                f.write("=" * 50 + "\n")
                f.write("\n感谢惠顾，欢迎下次再来！\n")

            print(f"收据已保存到文件: {filename}")
        except Exception as e:
            print(f"保存收据时出错: {e}")
        input("按Enter继续...")

    def run(self):
        """运行点菜系统"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "=" * 50)
            print(f"{'餐厅点菜系统'.center(48)}")
            print("=" * 50)
            print("1. 显示菜单")
            print("2. 添加菜品到订单")
            print("3. 从订单中移除菜品")
            print("4. 查看当前订单")
            print("5. 设置折扣")
            print("6. 生成收据")
            print("7. 保存收据到文件")
            print("8. 退出系统")
            print("=" * 50)

            choice = input("请输入您的选择（1-8）：").strip()

            if choice == '1':
                self.display_menu()
                input("按Enter返回主菜单...")
            elif choice == '2':
                self.add_to_order()
            elif choice == '3':
                self.remove_from_order()
            elif choice == '4':
                self.display_order()
                input("按Enter返回主菜单...")
            elif choice == '5':
                self.set_discount()
            elif choice == '6':
                self.generate_receipt()
            elif choice == '7':
                self.save_receipt_to_file()
            elif choice == '8':
                print("\n感谢使用餐厅点菜系统，再见！")
                sys.exit()
            else:
                print("无效的选择，请输入1-8之间的数字！")
                input("按Enter继续...")

if __name__ == "__main__":
    system = RestaurantOrderingSystem()
    system.run()