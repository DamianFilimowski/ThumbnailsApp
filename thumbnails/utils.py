def if_size_in_plan(size, plan):
    sizes = plan.plan.sizes.all()
    print(size)
    print(sizes)
    for s in sizes:
        if size == s.height:
            return True
    return False
