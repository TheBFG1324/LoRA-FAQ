import os, json, tensorflow as tf, keras, keras_hub
os.environ["KERAS_BACKEND"] = "tensorflow"

# hyperparams
PRESET = "gpt2_base_en"
EPOCHS = 2
BATCH = 8

# 1) load end-to-end LM (includes preprocessor)
lm = keras_hub.models.GPT2CausalLM.from_preset(PRESET)

# 2) enable LoRA on the backbone (PEFT)
lm.backbone.enable_lora(rank=8) 

# 3) build a simple tf.data over concatenated prompt+response strings
def gen():
    with open("data/quotes.jsonl") as f:
        for line in f:
            obj = json.loads(line)
            yield f"User: {obj['prompt']}\nAssistant: {obj['response']}"

ds = (tf.data.Dataset.from_generator(
          gen, output_signature=tf.TensorSpec(shape=(), dtype=tf.string))
      .shuffle(1024)
      .batch(BATCH)
      .prefetch(tf.data.AUTOTUNE))

# 4) compile & train
lm.compile(optimizer=keras.optimizers.Adam(2e-5))
lm.fit(ds, epochs=EPOCHS)

# 5) save
os.makedirs("artifacts", exist_ok=True)
lm.save("artifacts/lora_gpt2.keras")    
