# timeseries `{gen, store, query}`

`main.py -h` for usage info (example below)

`{gen,store,query}.py`'s main-block contains relevant unit & integration tests

1. [main.py](main.py)

    > interative parser, sample usage:
    1. Generate & store data of {10 symbols @ [20140301~20160329]}
    
        `./main.py --ops g s --n_syms 10 --d0 20140301 --d1 20160329`
        > data go into 'stored/[\$yyyy]/[\$mm]/data.csv'
        
    2. Query & store results on {symbols: {1,3,4} @ [20141115~20150708]}
    
        `./main.py --ops q s --q_syms 1,3,4 --d0 20141115 --d1 20150708`
        > results go into 'queried/[\$span]-[\$syms]'
        > e.g. 'queried/20141117_20150708-sym_1_sym_3_sym_4.csv'


1. [query.py](query.py)

    > maps timespan to file-path; concatenates then filters

    - `find(timespan, symbols)` mock index-lookup on distributed file-system
    - `stitch([df..])` mock reducer
    - TODO? validate input further


1. [store.py](store.py)

    > persist in hierarchical file-system that conceptually represents a distributed-system

    - shard by [year,month]
    - TODO? shard further by [sym]
    - `distribute(..)` mock mapper that shards an input data-stream then parcels out writing-tasks


1. [gen.py](gen.py)

    >mock price timeseries

    - timespan
    - ticker-symbol
    - `gen_sym2price(timespan, symbols)` Laplace-randomly-generate a price-series-over-timespan for each mock symbol


## TODO
- viz
- type- hints/check


