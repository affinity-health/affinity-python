# Reference
## Account
<details><summary><code>client.account.<a href="../src/affinity/account/client.py">get</a>() -> Account</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Read the organization and Test or Live mode selected by the API key.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.account.get()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Feedback
<details><summary><code>client.feedback.<a href="../src/affinity/feedback/client.py">create</a>(...) -> CreateFeedbackResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Send feedback without credentials, or with an API key to include its organization and mode. Do not include patient information. API-key callers are limited to 10 submissions per hour per key. Anonymous callers are limited to 10 submissions per hour per IP address. A 429 response includes Retry-After in seconds.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.feedback.create(
    idempotency_key="Idempotency-Key",
    message="The error does not explain which field is invalid.",
    page_url="https://docs.affinityrx.com/errors/",
    request_id="6e562761-eff3-4626-a8b9-25ce7c670ccd",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**message:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**page_url:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_id:** `typing.Optional[str]` — The `requestId` of the response, as the API returned it.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Medications
<details><summary><code>client.medications.<a href="../src/affinity/medications/client.py">list</a>(...) -> MedicationList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Every medication you can order in the current mode, A to Z by name, then by ID. The list has no search or filters: read every page and choose by name, strength, form and pharmacy. Prices are in cents. `requirements` names the optional prescription fields this pharmacy requires; `compoundingReasons` and `quantities` list the accepted values when the pharmacy limits them, counted in `quantityUnit`. With a `fill`, `price` is per fill and each quantity counts `quantityUnit`, not fills: it is a whole number of fills in units. For a fill of 30 tablets, quantity 60 is two fills. For vials, quantity 1 is one vial and quantity 2 is two vials. A 2 mL vial lists quantities 1–10; its volume is separate from its quantity.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.medications.list(
    practice_id="prac_01j2y8m6jcc9tt24af5pw9x1bc",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**practice_id:** `typing.Optional[str]` — Quote prices and availability for this practice. A platform may select only its own child practices; a practice may select only itself. Omit to use the caller's organization.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum records per page, from 1 to 100. Defaults to 25.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — Page forward using the previous response's nextCursor. Keep the same filters, sort, organization and mode.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.medications.<a href="../src/affinity/medications/client.py">get</a>(...) -> GetMedicationsResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Read one available medication, its pricing, and pharmacy details for the current organization and mode. Pass expand=variants to include its other strengths, forms and pharmacies.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.medications.get(
    medication_id="med_01j2y8m6jcc9tt24af5pw9x1bc",
    practice_id="prac_01j2y8m6jcc9tt24af5pw9x1bc",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**medication_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**practice_id:** `typing.Optional[str]` — Quote prices and availability for this practice. A platform may select only its own child practices; a practice may select only itself. Omit to use the caller's organization.
    
</dd>
</dl>

<dl>
<dd>

**expand:** `typing.Optional[typing.Union[GetMedicationsRequestExpandItem, typing.Sequence[GetMedicationsRequestExpandItem]]]` — Add related records to the response. `variants` adds the medication's other strengths, forms and pharmacies.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Orders
<details><summary><code>client.orders.<a href="../src/affinity/orders/client.py">list</a>(...) -> OrderList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List accessible orders in the current mode, newest first. `externalOrderId` matches exactly, including case. `updatedAfter` accepts an ISO 8601 timestamp with a timezone and returns strictly later updates. Keep filters fixed while paging. `sort` takes `patient` (lowercase firstName + space + lastName A to Z, then order ID) or `created` (oldest first); a `_desc` suffix reverses. Creation time or patient name and the order ID determine cursor order, even when updatedAt changes.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.orders.list(
    patient_id="pat_01j2y8m6jcc9tt24af5pw9x1bc",
    practice_id="prac_01j2y8m6jcc9tt24af5pw9x1bc",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum records per page, from 1 to 100. Defaults to 25.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — Page forward using the previous response's nextCursor. Keep the same filters, sort, organization and mode.
    
</dd>
</dl>

<dl>
<dd>

**external_order_id:** `typing.Optional[str]` — Match the external order ID exactly, including case. Combine with practiceId when your platform reuses IDs across practices.
    
</dd>
</dl>

<dl>
<dd>

**updated_after:** `typing.Optional[datetime.datetime]` — Return orders whose updatedAt is strictly later than this ISO 8601 timestamp. Sorting stays by creation time and ID unless sort is supplied. Keep this cutoff unchanged while paging.
    
</dd>
</dl>

<dl>
<dd>

**patient_id:** `typing.Optional[str]` — Limit results to the patient with this pat_ ID.
    
</dd>
</dl>

<dl>
<dd>

**practice_id:** `typing.Optional[str]` — Limit results to the practice with this prac_ ID, within your authorized practices.
    
</dd>
</dl>

<dl>
<dd>

**query:** `typing.Optional[str]` — Search saved order snapshots: patient names, email, phone and external ID; order external ID; prescriber name and NPI; medication names and brands; pharmacy name. Whole ord_ and pat_ IDs and six-character order numbers also match. Text matches ignore case and allow substrings, word prefixes and similar spellings for alphanumeric words of four or more characters. Every one of the first eight words containing letters or numbers must match; punctuation-only words are ignored. An empty or punctuation-only query leaves the list unfiltered. Date of birth, separate strength fields, practice names, prac_ IDs and rx_ IDs are not searched. Restart pagination when filters change.
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[ListOrdersRequestStatus]` — Return only orders with this status. Omit to include all statuses.
    
</dd>
</dl>

<dl>
<dd>

**cancel_requested:** `typing.Optional[ListOrdersRequestCancelRequested]` — true returns only submitted or processing orders with a cancel the pharmacy has not confirmed yet (cancelRequestedAt set). false leaves those orders out. Omit to include both.
    
</dd>
</dl>

<dl>
<dd>

**recently_shipped:** `typing.Optional[ListOrdersRequestRecentlyShipped]` — true returns only orders whose status is shipped and that shipped in the last 60 days; delivered orders are excluded. false leaves those orders out. Omit to include both.
    
</dd>
</dl>

<dl>
<dd>

**sort:** `typing.Optional[ListOrdersRequestSort]` — patient sorts the lowercase text firstName + space + lastName A to Z, then order ID; created sorts oldest first. A _desc suffix reverses the order. Defaults to created_desc. Restart pagination after changing sort.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="../src/affinity/orders/client.py">create</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

One request creates the order, signs it and sends it to the pharmacy. Platforms must send practiceId; practice callers can omit it to use their own practice. With an API key, name the prescriber and send signatureAttestation. Optional prescriber phone and address each default to the practice; no account is looked up by NPI. In the app, the signed-in member signs with the NPI in their settings, or names the prescriber with the same attestation. The patient is found by patient.externalId and updated from the order. Live orders require Live access on the practice and its platform. No payment method is required.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity, PatientInput, AddressInput, PatientInputAllergiesItem, PrescriptionInput
from affinity.environment import AffinityEnvironment
from affinity.orders import OrderInputShipping

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.orders.create(
    idempotency_key="Idempotency-Key",
    patient=PatientInput(
        address=AddressInput(
            line1="line1",
            city="city",
            state="state",
            postal_code="postalCode",
        ),
        allergies=[
            PatientInputAllergiesItem(
                category="drug",
                display="display",
            )
        ],
        date_of_birth="dateOfBirth",
        email="email",
        first_name="firstName",
        sex="female",
        last_name="lastName",
        phone="phone",
    ),
    prescriptions=[
        PrescriptionInput(
            directions="directions",
            medication_id="med_01j2y8m6jcc9tt24af5pw9x1bc",
            quantity=1,
            refills=1,
        )
    ],
    shipping=OrderInputShipping(
        option_id="shp_01j2y8m6jcc9tt24af5pw9x1bc",
    ),
    signature_attestation=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**patient:** `PatientInput` 
    
</dd>
</dl>

<dl>
<dd>

**prescriptions:** `typing.List[PrescriptionInput]` — The 1 to 20 prescriptions approved for this patient.
    
</dd>
</dl>

<dl>
<dd>

**shipping:** `OrderInputShipping` — The shipping option and destination.
    
</dd>
</dl>

<dl>
<dd>

**signature_attestation:** `bool` — Must be true to attest that the named prescriber approved and signed these prescriptions.
    
</dd>
</dl>

<dl>
<dd>

**external_order_id:** `typing.Optional[str]` — Your order identifier, unique within the practice and mode.
    
</dd>
</dl>

<dl>
<dd>

**practice_id:** `typing.Optional[str]` — Required with a platform API key. Send a child practice ID. Independent practice keys can omit this field to use their own practice.
    
</dd>
</dl>

<dl>
<dd>

**prescriber:** `typing.Optional[PrescriberInput]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="../src/affinity/orders/client.py">get</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Read one order and its prescriptions in the API key's organization and mode.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.orders.get(
    order_id="ord_01j2y8m6jcc9tt24af5pw9x1bc",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**order_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.orders.<a href="../src/affinity/orders/client.py">cancel</a>(...) -> Order</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

200 with status cancelled when the cancel is confirmed. 202 with cancelRequestedAt when the pharmacy has not confirmed yet: you get order.cancelled when it confirms, or, when it refuses, cancelRequestedAt becomes null and you get order.updated. 409 when the pharmacy refuses or the order has shipped.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.orders.cancel(
    order_id="ord_01j2y8m6jcc9tt24af5pw9x1bc",
    idempotency_key="Idempotency-Key",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**order_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Practices
<details><summary><code>client.practices.<a href="../src/affinity/practices/client.py">list</a>(...) -> PracticeList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the platform's practices, newest first. Available to platforms only. `sort` takes `name` or `location` (A to Z, practices without a location last), `mode` (Test before Live) or `created` (oldest first); a `_desc` suffix reverses.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.practices.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum records per page, from 1 to 100. Defaults to 25.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — Page forward using the previous response's nextCursor. Keep the same filters, sort, organization and mode.
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `typing.Optional[str]` — Match the external practice ID exactly, including case. Keep this filter unchanged while paging.
    
</dd>
</dl>

<dl>
<dd>

**query:** `typing.Optional[str]` — Match practice names containing this text, ignoring case. Restart pagination after changing query.
    
</dd>
</dl>

<dl>
<dd>

**sort:** `typing.Optional[ListPracticesRequestSort]` — name and location sort A to Z; mode sorts Test before Live; created sorts oldest first. A _desc suffix reverses the order. Defaults to created_desc. Missing locations sort last. Restart pagination after changing sort.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.practices.<a href="../src/affinity/practices/client.py">create</a>(...) -> Practice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Platforms only. Name, phone and address are required. The practice starts in Test; `liveEnabled: true` also allows new Live orders, which needs a platform with Live access and a Live caller: a Live key, or a session in Live mode. Turning Live off later preserves access to existing records. A retry with the same key and body returns the stored first response, even if the practice has changed. Use GET /v1/practices/{practiceId} to read the current practice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity, AddressInput
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.practices.create(
    idempotency_key="Idempotency-Key",
    address=AddressInput(
        line1="line1",
        city="city",
        state="state",
        postal_code="postalCode",
    ),
    name="name",
    phone="phone",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**address:** `AddressInput` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**phone:** `str` — A US phone number: 10 digits, with or without +1 or 1 before them. Spaces, dashes, dots and parentheses are allowed, such as (512) 555-0100. Affinity stores and returns +15125550100.
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `typing.Optional[str]` — Your practice identifier, unique among your platform's active practices.
    
</dd>
</dl>

<dl>
<dd>

**live_enabled:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.practices.<a href="../src/affinity/practices/client.py">get</a>(...) -> Practice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Read one practice accessible to the API key. A platform can read its own practices.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.practices.get(
    practice_id="prac_01j2y8m6jcc9tt24af5pw9x1bc",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**practice_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.practices.<a href="../src/affinity/practices/client.py">update</a>(...) -> Practice</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

`liveEnabled` allows or refuses new Live orders. Existing records, cancellation, webhooks and billing keep working. Only its platform changes it; enabling requires platform Live access, and either change needs a Live caller: a Live key (403 live_key_required otherwise) or a session in Live mode (403 live_mode_required otherwise). Live orders send `name`, `phone` and `address` to the pharmacy, so a practice with Live access changes them only with a Live key (403 live_mode_required otherwise). A retry with the same key and body returns the stored first response, even if the practice has changed. Use GET /v1/practices/{practiceId} to read the current practice.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.practices.update(
    practice_id="prac_01j2y8m6jcc9tt24af5pw9x1bc",
    idempotency_key="Idempotency-Key",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**practice_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `typing.Optional[str]` — Your practice identifier, unique among your platform's active practices. Send null to clear it.
    
</dd>
</dl>

<dl>
<dd>

**address:** `typing.Optional[UpdatePracticesRequestAddress]` 
    
</dd>
</dl>

<dl>
<dd>

**live_enabled:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**phone:** `typing.Optional[str]` — A US phone number: 10 digits, with or without +1 or 1 before them. Spaces, dashes, dots and parentheses are allowed, such as (512) 555-0100. Affinity stores and returns +15125550100. Empty text counts as null.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Webhooks
<details><summary><code>client.webhooks.<a href="../src/affinity/webhooks/client.py">list</a>(...) -> WebhookEndpointList</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List webhook endpoints owned by the API key's organization in its current mode. Signing secrets are not returned.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.webhooks.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum records per page, from 1 to 100. Defaults to 25.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — Page forward using the previous response's nextCursor. Keep the same filters, sort, organization and mode.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="../src/affinity/webhooks/client.py">create</a>(...) -> CreateWebhooksResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Platforms and independent practices can register up to 16 public HTTPS endpoints per mode. An API key acts only for its own organization and mode. Every event goes to every endpoint. The signing secret is returned by creation and its idempotent replay for 24 hours.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.webhooks.create(
    idempotency_key="Idempotency-Key",
    url="url",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**url:** `str` — The public HTTPS URL that receives webhook events.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="../src/affinity/webhooks/client.py">remove</a>(...) -> RemoveWebhooksResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Events not delivered to it yet are dropped.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.webhooks.remove(
    webhook_endpoint_id="whe_01j2y8m6jcc9tt24af5pw9x1bc",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_endpoint_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="../src/affinity/webhooks/client.py">update</a>(...) -> WebhookEndpoint</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

The signing secret stays the same.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.webhooks.update(
    webhook_endpoint_id="whe_01j2y8m6jcc9tt24af5pw9x1bc",
    idempotency_key="Idempotency-Key",
    url="url",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_endpoint_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**url:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="../src/affinity/webhooks/client.py">resend_failed</a>(...) -> ResendFailedWebhooksResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Queue failed order event deliveries from the last 30 days for this endpoint. Only the current organization and mode apply. Each failed delivery gets up to 12 new attempts. Also make pending deliveries waiting on a later retry due now, without resetting their attempt counts. Keep the same event IDs, payloads, and per-order delivery sequence. The queued count includes both kinds. Pending deliveries already due, delivered events, and one-time test events stay unchanged. Send a unique Idempotency-Key for each request. Reuse that key after an uncertain response to return the original count. A request with a new key returns 0 when no eligible failures or pending deliveries waiting on a later retry remain.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from affinity import Affinity
from affinity.environment import AffinityEnvironment

client = Affinity(
    token="<token>",
    environment=AffinityEnvironment.DEFAULT,
)

client.webhooks.resend_failed(
    webhook_endpoint_id="whe_01j2y8m6jcc9tt24af5pw9x1bc",
    idempotency_key="Idempotency-Key",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_endpoint_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**idempotency_key:** `str` — A unique key per operation, 1 to 255 printable ASCII characters without spaces. Retry the same key and body to avoid repeating the action. The replay response depends on the operation. See https://docs.affinityrx.com/guides/#retry-safely.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

