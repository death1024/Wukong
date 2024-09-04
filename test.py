import asyncio



async def acc():
    if m<=100:
        m+=1

async def bcc():
    if n<=100:
        n+=1


async def main():
    await asyncio.gather(acc(), bcc())

    print(acc.m,bcc.n)

if __name__ == '__main__':
    main()