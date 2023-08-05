#include <stdio.h>
#include <assert.h>
#include "thread-test.h"

#define NTHREADS 10


extern int add1(int, int);

static sem_t done;


static void *start_routine(void *arg)
{
    int i, x, expected, status;

    expected = add1(40, 2);
    assert((expected % 1000) == 42);

    for (i=0; i<10; i++) {
        x = add1(50, i);
        assert(x == expected + 8 + i);
    }

    status = sem_post(&done);
    assert(status == 0);

    return arg;
}

int main(void)
{
    pthread_t th;
    int i, status = sem_init(&done, 0, 0);
    assert(status == 0);

    for (i = 0; i < NTHREADS; i++) {
        status = pthread_create(&th, NULL, start_routine, NULL);
        assert(status == 0);
    }
    for (i = 0; i < NTHREADS; i++) {
        status = sem_wait(&done);
        assert(status == 0);
    }
    printf("done\n");
    return 0;
}
