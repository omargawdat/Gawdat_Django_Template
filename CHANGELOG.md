# CHANGELOG


## v0.10.0 (2025-02-21)

### Features

- Add local .env
  ([`a3e772d`](https://github.com/omargawdat/Gawdat_Django_Template/commit/a3e772d290bb39e7fa6f76a1237595218d2a4be1))

### Refactoring

- Remove allowed hosts
  ([`dd20602`](https://github.com/omargawdat/Gawdat_Django_Template/commit/dd2060295b51ffaf6fc1828c9330e0aea9542524))


## v0.9.0 (2025-02-20)

### Bug Fixes

- Allowed hosts
  ([`f97711d`](https://github.com/omargawdat/Gawdat_Django_Template/commit/f97711d013dac9fd9e028e17d5ea61e4f2944a60))

- Remove
  ([`4819054`](https://github.com/omargawdat/Gawdat_Django_Template/commit/4819054211ee4bce80b12796f79be62b7ecfe0ae))

### Chores

- Update pydantic
  ([`60b02fd`](https://github.com/omargawdat/Gawdat_Django_Template/commit/60b02fd1f48b91520ae8cf04462d6ebe907cd159))

### Features

- Add pydantic
  ([`1be8c86`](https://github.com/omargawdat/Gawdat_Django_Template/commit/1be8c86a9679597a78db7838b2ab32e6b622edec))

- Checkout
  ([`e37faa7`](https://github.com/omargawdat/Gawdat_Django_Template/commit/e37faa7da8dc82a89a18c3a1f9ba94c6651760b1))

- Checkout
  ([`781ae61`](https://github.com/omargawdat/Gawdat_Django_Template/commit/781ae6139b3e8a79d92cc224a283a5863406d0cc))

- Checkout
  ([`db8b3cc`](https://github.com/omargawdat/Gawdat_Django_Template/commit/db8b3cc8ca6e84e37c77b4d2c9cf4d4442e92690))

- Load aws secrets
  ([`9c3df10`](https://github.com/omargawdat/Gawdat_Django_Template/commit/9c3df104d5c07491b654b4e619e0c7d411974d36))

- Pass environment into the container
  ([`6cb9ce0`](https://github.com/omargawdat/Gawdat_Django_Template/commit/6cb9ce072f9ccf0273e2e8d68480d6be1fdac6d9))

- Working refactor
  ([`b9268bb`](https://github.com/omargawdat/Gawdat_Django_Template/commit/b9268bb68234ad49cdb092428818e998e4977886))


## v0.8.0 (2025-01-24)

### Chores

- Collect settings helper methods
  ([`a50b77d`](https://github.com/omargawdat/Gawdat_Django_Template/commit/a50b77d0d3ed77d4f646550460cf44e54be0df95))

- Update github action versions
  ([`83949e6`](https://github.com/omargawdat/Gawdat_Django_Template/commit/83949e663dd9e285043374847374c0e45ff1703b))

### Features

- Ensure api key passed
  ([`f3d1be6`](https://github.com/omargawdat/Gawdat_Django_Template/commit/f3d1be6ee2acaebd89d98b2e96adcdcf1f2a568c))

### Refactoring

- Checkout
  ([`625f53a`](https://github.com/omargawdat/Gawdat_Django_Template/commit/625f53a6393c77024bb83e94d9939d9a86fe51ab))

- Checkout
  ([`4b3541e`](https://github.com/omargawdat/Gawdat_Django_Template/commit/4b3541e625f769b05080f0c6946dc1f943e30252))


## v0.7.0 (2025-01-15)

### Features

- Enable cors for websites
  ([`1504deb`](https://github.com/omargawdat/Gawdat_Django_Template/commit/1504deb289f4c5fcc48edd88c75b16b5c4d319cd))

### Refactoring

- Cleaner convert error message
  ([`82f4422`](https://github.com/omargawdat/Gawdat_Django_Template/commit/82f4422d671beb0d3fc632aeaa0feae8e6ce5ed1))

- Get the domain name from the .env file
  ([`2416e19`](https://github.com/omargawdat/Gawdat_Django_Template/commit/2416e19a15372155589b928e453d31b99928ba2f))

- Restructure the settings into more cleaner way
  ([`cc1951f`](https://github.com/omargawdat/Gawdat_Django_Template/commit/cc1951f86f22e23845798d166155b2ac0fe07dfd))


## v0.6.0 (2025-01-12)

### Chores

- Empty
  ([`e6a651d`](https://github.com/omargawdat/Gawdat_Django_Template/commit/e6a651df74c8ab9b30df89f670045934b84532cd))

### Features

- Only require api-key on endpoints that require permissions
  ([`9de845b`](https://github.com/omargawdat/Gawdat_Django_Template/commit/9de845bd2b51d5a03ba5fd8e83893c7a33842d45))

### Refactoring

- Enhance code
  ([`488ce03`](https://github.com/omargawdat/Gawdat_Django_Template/commit/488ce032c704871cbb22fc268342a8a359adcebb))


## v0.5.0 (2025-01-10)

### Chores

- Add openpyxl package
  ([`739642f`](https://github.com/omargawdat/Gawdat_Django_Template/commit/739642f3aa6baefb59b2ea9de46571e35163af4c))

- Add openpyxl package
  ([`0c3592e`](https://github.com/omargawdat/Gawdat_Django_Template/commit/0c3592e661c8d53170282d4a608441bd31f969b6))

### Features

- Better error handling in only the model
  ([`961091e`](https://github.com/omargawdat/Gawdat_Django_Template/commit/961091ec1a068bb5d364689f492ac870f770aab1))


## v0.4.0 (2024-12-22)

### Bug Fixes

- Expost local postgres port
  ([`3adacd6`](https://github.com/omargawdat/Gawdat_Django_Template/commit/3adacd62ba96eaf2a986a560a46cb00bc38f27b4))

### Features

- Make the validation of the endpoints only inside the restframework
  ([`e04e826`](https://github.com/omargawdat/Gawdat_Django_Template/commit/e04e82624325b6eb522040f5852aeed0ca4ede07))

- Make validation inside api instead of middleware
  ([`61c67f0`](https://github.com/omargawdat/Gawdat_Django_Template/commit/61c67f0ed788e83b5a566622938624e4dd721773))


## v0.3.0 (2024-12-22)

### Documentation

- Add dummy space
  ([`d0ad911`](https://github.com/omargawdat/Gawdat_Django_Template/commit/d0ad911870742a37b6d09c9dbacf7d9cb9fdba65))

### Features

- Update model admin base to handle the form errors in a better way
  ([`966a1ae`](https://github.com/omargawdat/Gawdat_Django_Template/commit/966a1ae702b2e88eae50f41d944ffe8df93a789d))


## v0.2.0 (2024-12-18)

### Features

- Get jwt tokens lifetime from .env file
  ([`fcdee5f`](https://github.com/omargawdat/Gawdat_Django_Template/commit/fcdee5fafbb773cf06c63b0f86d7560a68141ba8))


## v0.1.1 (2024-12-17)

### Bug Fixes

- Install hadolint
  ([`c5fe626`](https://github.com/omargawdat/Gawdat_Django_Template/commit/c5fe626eff339d8032863094b816928ed3f18c32))


## v0.1.0 (2024-12-17)

### Bug Fixes

- Doc docker container error missing git
  ([`14fa1b8`](https://github.com/omargawdat/Gawdat_Django_Template/commit/14fa1b81dac1d4cc16039dd63315c1e95b6fd5fa))

### Features

- Init commit
  ([`3fb3ac0`](https://github.com/omargawdat/Gawdat_Django_Template/commit/3fb3ac0469293a69d2110611d97a63965f8726ef))
