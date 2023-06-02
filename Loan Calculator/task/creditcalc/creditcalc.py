import math
import argparse
import sys

parser = argparse.ArgumentParser();
parser.add_argument('--type', choices=['diff', 'annuity'], help='choose between differentiated and annuity payment')
parser.add_argument('--principal', type=int, help='loan principal')
parser.add_argument('--periods', type=int, help='number of payments')
parser.add_argument('--interest', type=float, help='annual interest rate')
parser.add_argument('--payment', type=float, help='the payment per months (annuity payment only)')
args = parser.parse_args()


def print_error():
    print("Incorrect parameters")
    exit(1)


def print_overpayment(principal, overall_payment):
    print(f'Overpayment = {int(round(overall_payment - principal))}')


if len(sys.argv) < 5:
    print_error()

if args.type == 'diff':
    if args.payment is not None:
        print_error()
    else:
        principal = int(args.principal)
        periods = int(args.periods)
        interest = float(args.interest)
        rate = interest / 100 / 12
        overall_payment = 0
        for m in range(1, periods + 1):
            payment = math.ceil(principal / periods + rate * (principal - principal * (m - 1) / periods))
            print(f'Month {m}: payment is {payment}')
            overall_payment += payment
        print()
        print_overpayment(principal, overall_payment)

elif args.type == 'annuity':
    if args.periods is None:
        principal = args.principal
        payment = args.payment
        interest = args.interest
        rate = interest / 100 / 12
        periods = int(math.ceil(math.log(payment / (payment - rate * principal), 1 + rate)))
        years = periods // 12
        months = periods % 12
        if years == 0:
            print(f'It will take {months} months to repay this loan')
        elif periods == 0:
            print(f'It will take {years} years to repay this loan')
        else:
            print(f'It will take {years} years and {months} months to repay this loan')
        print_overpayment(principal, payment * periods);
    elif args.payment is None:
        principal = args.principal
        periods = args.periods
        interest = args.interest
        rate = interest / 100 / 12
        payment = math.ceil(principal * rate * math.pow(1 + rate, periods) / (math.pow(1 + rate, periods) - 1))
        print(f'Your annuity payment = {payment}!')
        print_overpayment(principal, payment * periods)
    elif args.principal is None:
        payment = args.payment
        periods = args.periods
        interest = args.interest
        rate = interest / 100 / 12
        principal = int(round(payment / (rate * math.pow(1 + rate, periods) / (math.pow(1 + rate, periods) - 1))))
        print(f'Your loan principal = {principal}!')
        print_overpayment(principal, payment * periods)
    elif args.interest is None:
        print_error()
else:
    print_error()
