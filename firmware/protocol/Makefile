# Include the nanopb provided Makefile rules
include ../nanopb/extra/nanopb.mk

# Build rule for the protocol
donglepi.pb.c: ../../protocol/donglepi.proto
	cd ../nanopb/generator/proto; make
	$(PROTOC) $(PROTOC_OPTS) --nanopb_out=. -I../../protocol -I../../firmware/nanopb/generator/proto ../../protocol/donglepi.proto

clean:
	rm -f donglepi.pb.c
	rm -f donglepi.pb.h
