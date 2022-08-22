import asyncio

MAX_PARALLEL_NETWORK_REQUESTS = 10
PAGINATION_SIZE = 100


async def paginate(
        total,
        async_paginate_fn,
        on_paginated,
        num_parallel_requests=MAX_PARALLEL_NETWORK_REQUESTS,
        pagination_size=PAGINATION_SIZE
):
    if total == 0:
        return

    batch_offset_increments = min(total, num_parallel_requests * pagination_size)

    for batch_offset in range(0, total, batch_offset_increments):
        response_batch = await asyncio.gather(*[
            async_paginate_fn(cur_offset, pagination_size) for cur_offset in range(
                batch_offset,
                min(batch_offset + batch_offset_increments, total),
                pagination_size
            )
        ])

        for response in response_batch:
            on_paginated(response)
