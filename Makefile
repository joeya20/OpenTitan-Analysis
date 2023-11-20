CXX := g++
CXX_FLAGS := -Wall -std=c++20 -I/home/joey/boost_1_83_0
LD_FLAGS := -lsvlang -lfmt -lmimalloc
SRC_PATH := src

sv_diff: $(SRC_PATH)/driver.cpp $(SRC_PATH)/DiffVisitor.hpp
	$(CXX) $(CXX_FLAGS) -o $@ $< $(LD_FLAGS)

.PHONY: clean
clean:
	-rm sv_diff