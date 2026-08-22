BUILD_DIR ?= build
ARTIFACT := $(BUILD_DIR)/artifact.txt
VERSION_FILE := VERSION
PAYLOAD := src/payload.txt

.PHONY: all clean

all: $(ARTIFACT)

$(ARTIFACT): $(VERSION_FILE) $(PAYLOAD) Makefile
	@mkdir -p "$(BUILD_DIR)"
	@{ \
		printf 'version=%s\n' "$$(cat "$(VERSION_FILE)")"; \
		printf 'source_sha256=%s\n' "$$(sha256sum "$(PAYLOAD)" | cut -d ' ' -f 1)"; \
		cat "$(PAYLOAD)"; \
	} > "$(ARTIFACT)"

clean:
	@rm -f "$(ARTIFACT)"
