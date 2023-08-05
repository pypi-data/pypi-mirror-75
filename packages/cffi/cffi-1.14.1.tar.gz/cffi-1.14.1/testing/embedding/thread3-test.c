#include <stdio.h>
#include <assert.h>
#include "thread-test.h"

extern int add2(int, int, int);
extern int add3(int, int, int, int);

static sem_t done;


static void *start_routine_2(void *arg)
{
    int x, status;
    x = add2(40, 2, 100);
    assert(x == 142);

    status = sem_post(&done);
    assert(status == 0);

    return arg;
}

static void *start_routine_3(void *arg)
{
    int x, status;
    x = add3(1000, 200, 30, 4);
    assert(x == 1234);

    status = sem_post(&done);
    assert(status == 0);

    return arg;
}

int main(void)
{
    pthread_t th;
    int i, status = sem_init(&done, 0, 0);
    assert(status == 0);

    printf("starting\n");
    fflush(stdout);
    for (i = 0; i < 10; i++) {
        status = pthread_create(&th, NULL, start_routine_2, NULL);
        assert(status == 0);
        status = pthread_create(&th, NULL, start_routine_3, NULL);
        assert(status == 0);
    }
    for (i = 0; i < 20; i++) {
        status = sem_wait(&done);
        assert(status == 0);
    }
    printf("done\n");
    fflush(stdout);   /* this is occasionally needed on Windows */
    return 0;
}
