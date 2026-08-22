BUILD_DIR ?= build
ARTIFACT := $(BUILD_DIR)/artifact.txt

.PHONY: all clean FORCE

all: $(ARTIFACT)

$(ARTIFACT): FORCE
	@mkdir -p "$(BUILD_DIR)"
	@{ \
		echo "version=$$(cat VERSION)"; \
		echo "built_at=$$(date -u +%Y-%m-%dT%H:%M:%SZ)"; \
		cat src/payload.txt; \
	} > "$(ARTIFACT)"

FORCE:

clean:
	@rm -f "$(ARTIFACT)"
