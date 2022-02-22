SRCS = $(wildcard *.c)
PROGS = $(patsubst %.c,%,$(SRCS))
CFLAGS = -O2 -Wall -lm

all: $(PROGS)

%: %.c
	$(CC) -o $@ $< $(CFLAGS)

clean:
	rm -f $(PROGS)

