# Usage

Once `mailer` is deployed, either on your own custom domain or locally, you can
start receiving e-mails, using a URL-encoded or an AJAX request.

Given that these features are enabled with your deployment, the following options are available:

- [Google ReCaptcha v2](https://developers.google.com/recaptcha/docs/display): make sure only your domains can send e-mails through `mailer`
- PGP public key attachment: so that you can respond with end-to-end encryption to your contacts!

## Parameters

You can find the documentation for the request parameters in the API documention
of your deployment (e.g. `https://mailer.domain.me/redoc`).

| Variable               | Default |           Format           | Description                                                      |
| ---------------------- | :-----: | :------------------------: | ---------------------------------------------------------------- |
| `name`                 |  `""`   |  `string, max length: 50`  | (**required**) Name of the contact sending the message           |
| `email`                |  `""`   |   `string, valid e-mail`   | (**required**) E-mail of the contact sending the message         |
| `subject`              |  `""`   | `string, max length: 100`  | (**required**) Subject of the message to send                    |
| `message`              |  `""`   | `string, max length: 1000` | (**required**) Body of the message to send                       |
| `honeypot`             |  `""`   |      `string, empty`       | (**required**) Body of the message to send                       |
| `g-recaptcha-response` |  `""`   |          `string`          | (**optional**) Google ReCaptcha v2 response                      |
| `public_key`           |  `""`   |          `string`          | (**optional**) PGP public key of the contact sending the message |

## Headers

When using AJAX requests, make sure the `Origin` header matches one of the domains
specified in the `CORS_ORIGINS` configuration of your deployment.

## HTML Form

Using a standard HTML form to perform an URL-encoded request:

```html
<form action="https://mailer.domain.me/api/mail/form" method="POST">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" />
  <br />
  <label for="email">E-mail</label>
  <input type="email" id="email" name="email" />
  <br />
  <label for="subject">Subject</label>
  <input type="text" id="subject" name="subject" />
  <br />
  <label for="message">Message</label>
  <input type="text" id="message" name="message" />
  <br />
  <input type="hidden" id="honeypot" name="honeypot" />
  <input type="submit" value="Send" />
</form>
```

## Fetch API

Using the [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) to perform an AJAX request:

```js
fetch("https://mailer.domain.me/api/mail", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email: "john@doe.com",
    name: "John Doe",
    subject: "Contact",
    message: "Hey there! Up for a coffee?",
    "g-recaptcha-response": "azertyuiopqsdfghjklmwxcvbn",
    public_key:
      "-----BEGIN PGP PUBLIC KEY BLOCK-----\n...\n-----END PGP PUBLIC KEY BLOCK-----\n",
    honeypot: "",
  }),
});
```

## Axios

Using [Axios](https://github.com/axios/axios) to perform an AJAX request:

```js
axios.post("https://mailer.domain.me/api/mail", {
  email: "john@doe.com",
  name: "John Doe",
  subject: "Contact",
  message: "Hey there! Up for a coffee?",
  "g-recaptcha-response": "azertyuiopqsdfghjklmwxcvbn",
  public_key:
    "-----BEGIN PGP PUBLIC KEY BLOCK-----\n...\n-----END PGP PUBLIC KEY BLOCK-----\n",
  honeypot: "",
});
```

## Examples

Explore ready-to-use examples to demonstrate how to use `mailer` in the `docs/examples` folder.

To run the examples properly, do not just open the `.html` files, but be sure
to server them with a basic HTTP server, for instance:

```bash
python -m http.server <port>
```

The reason for this requirement is that if you enable CORS protection on `mailer`,
opening files directly in a web-browser will not set the `Origin` header properly,
thus all requests will fail.

Be sure to configure and run an instance of `mailer` before using them!

- [Simple AJAX form](examples/simple-ajax.html)
- [Simple AJAX form with Google ReCaptcha](examples/simple-ajax-recaptcha.html)
- [Simple AJAX form with PGP encryption](examples/simple-ajax-pgp.html)
